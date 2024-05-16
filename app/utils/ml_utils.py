import numpy as np
import pandas as pd
from itertools import product

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
# import matplotlib.pyplot as plt

from app.config import ml_conf
from app.utils.logger import logger
from app.errors import SupportError


def can_convert_to_number(s):
    try:
        float(s)  # 尝试将字符串转换为浮点数
        return True
    except ValueError:
        return False
    
    
def normalized(X):
    if ml_conf.USE_NORMALIZED:
        X_scaled = StandardScaler().fit_transform(X)
    else:
        X_scaled = X
    return X_scaled


# 定义最优的标准
def evaluate_mape(y_true, y_pred):
    y_true = np.array(y_true).flatten()
    y_pred = np.array(y_pred).flatten()
    mape = np.mean(np.abs((y_true - y_pred) / y_true))
    accuracy = 1 - mape
    return accuracy


def material_importance(X, y, function_name="RandomForest"):
    '''
    用随机森林生成物料权重。
    '''
    X_scaled = normalized(X)

    match function_name:
        case "RandomForest":
            rf = RandomForestRegressor(max_depth=5, n_estimators=100, random_state=0)
            rf.fit(X_scaled, y)
        case _:
            raise SupportError

    # 物料权重的numpy数组
    importance = rf.feature_importances_

    return importance


def correlation(df, method):
    # 获取表格数据的相关性矩阵
    correlation = df.corr(method=method)
    # plt.matshow(correlation)
    # plt.show()
    correlation = correlation.fillna(0)

    return correlation


def separated_y(file):
    '''
    遍历分类号好的数据集，返回包含单列检测结果的文件。
    '''
    df = pd.read_json(file)
    df.dropna(axis=1, how='all', inplace=True)  # 删除空列
    X_columns = [col for col in df.columns if 'M' in col]
    y_columns = [col for col in df.columns if 'Q' in col]

    # 将X与Y1, Y2, Y3分别拼起来
    xy_separated = {}
    for i in df[y_columns].columns:
        xy = pd.concat([df[X_columns], df[y_columns][i]], axis=1)
        xy1 = xy.loc[xy.iloc[:, -1] != 0]
        xy_separated[i] = xy1

    return xy_separated


def calculate_distance(X, Y, method="euclidean"):
    """
    计算距离
    """
    match method:
        case "euclidean":
            distances = euclidean_distances(X, Y)
        case _:
            raise SupportError
    return distances


# 定义一个生成器函数，它逐批处理records迭代器中的每个元组
def batch_records_generator(records, columns, batch_size=100):
    batch_records = []
    for record in records:
        # 四舍五入到指定的小数位数，然后转换为DataFrame
        df = pd.DataFrame([tuple(round(x, 4) for x in record)], columns=columns)
        batch_records.append(df)
        
        # 当记录的数量达到batch_size时，生成当前批次的DataFrame
        if len(batch_records) == batch_size:
            yield pd.concat(batch_records, ignore_index=True)
            batch_records = []  # 清空批次记录，为下一批做准备
    
    # 如果最后一批记录的数量小于batch_size，也生成它
    if batch_records:
        yield pd.concat(batch_records, ignore_index=True)


def piecewise_sampling(column_names, lower_bound, upper_bound, piecewise_cnt):
    """
    分段采样

    Arguments:
    - column_names: dataframe的columns
    - lower_bound: 物料下界
    - upper_bound: 物料上界
    - piecewise_cnt: 段数, 经测试, 建议物料种类大于30时取2, 小于30时取3
    """
    # 为X的每个分量生成m个段，但对于相同上下限的分量不进行切割操作
    X_segments = []
    for X_min, X_max in zip(lower_bound, upper_bound):
        logger.logger.debug(X_min, X_max)
        if X_min == X_max:
            # 对于相同上下限的分量，直接添加到X_segments中
            X_segments.append(np.array([X_min]))
        else:
            X_segments.append(np.linspace(X_min, X_max, piecewise_cnt))

    num_combinations = 1
    for segment in X_segments:
        num_combinations *= len(segment)
    logger.logger.info(f"The number of Cartesian products: {str(num_combinations)}")

    combinations_iterator = product(*X_segments)
    rounded_product = (np.round(arr, decimals=4) for arr in combinations_iterator)

    # 避免内存爆炸，这里只提取100万种组合
    new_df = pd.DataFrame.from_records(rounded_product, columns=column_names, coerce_float=True, nrows=1000000)

    return new_df


def metropolis_hastings_sampling(column_names, lower_bounds, upper_bounds, mean, cov, n_samples, n_burnin=1000, proposal_scale=1.0):
    """
    使用Metropolis-Hastings算法从多维正态分布中采样。
    
    参数:
    - mean: 目标多维正态分布的均值向量。
    - cov: 目标多维正态分布的协方差矩阵。
    - lower_bounds: 每个维度的下界列表。
    - upper_bounds: 每个维度的上界列表。
    - n_samples: 要生成的样本数量。
    - n_burnin: 烧入期（丢弃的初始样本数量）。
    - proposal_scale: 提案分布的标准差（基于目标分布的标准差）。
    
    返回:
    - df: 形状为 (n_samples, len(mean)) 的数组，包含接受的样本。
    - accept_rate: 采样过程中的接受率
    """
    # 计算目标分布的尺度（标准差）
    target_std = np.sqrt(np.diag(cov))
    
    # 初始化参数
    current_sample = np.random.uniform(lower_bounds, upper_bounds, size=len(column_names))
    n_accepted = 0
    
    # 存储接受的样本
    samples = []
    
    for i in range(n_samples + n_burnin):
        # 提出一个新的样本
        proposed_sample = np.random.normal(current_sample, proposal_scale * target_std)
        
        # 确保提议的样本在界限内
        proposed_sample = np.clip(proposed_sample, lower_bounds, upper_bounds)
        
        # 计算接受比率
        # 由于我们从正态分布中采样，我们不需要显式计算目标分布的密度
        # 因为提议分布和目标分布的比率差会被标准化
        acceptance_ratio = min(1, np.exp(np.sum(np.log(proposal_scale * target_std)) - np.sum(np.log(target_std))))  # 正确的接受比率计算
        
        # 接受或拒绝提议的样本
        if np.random.rand() < acceptance_ratio:
            current_sample = proposed_sample  # 接受提议的样本
            n_accepted += 1
            if i >= n_burnin:
                # 对接受的样本进行四舍五入
                rounded_sample = np.round(current_sample, decimals=ml_conf.decimal_places)
                samples.append(rounded_sample)
    
    accept_rate = n_accepted / (n_samples)
    logger.logger.info(f"Metropolis hastings acceptance rate is {str(accept_rate)}")
    # 将样本列表转换为NumPy数组
    samples_array = np.array(samples)
    
    # 创建DataFrame
    df = pd.DataFrame(samples_array, columns=column_names)
    
    return df, accept_rate