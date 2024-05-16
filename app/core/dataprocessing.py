"""
Description:
    - 调用后端接口
    1. 获取配方数据
    2. 模型地址
    3. 自变量上下界

    - 配方编码
    - 指标编码
"""
from app.utils.database import search
from app.models import repos_orms
from app.utils.logger import logger


async def read_all_data_from_db(ids=None, db=None):
    logger.logger.info("read model from db ...")
    if ids and len(ids) > 0:
        properties = await search(
                            db, 
                            repos_orms.Properties, 
                            repos_orms.Properties.Id.in_(ids)
                    )
    else:
        properties = await search(
                            db, 
                            repos_orms.Properties, 
                    )
    return properties


async def format_reponse_body(cluster_res, dataframe):
    # 创建一个字典{类别1:[id1, id2, ...],}
    label_indices = dict()
    for label in range(-1, max(cluster_res.labels_) + 1):
        label_indices[label] = [i for i, value in enumerate(cluster_res.labels_) \
                                if value == label]
        
    datasets = []
    for label in range(-1, max(cluster_res.labels_) + 1):
        logger.logger.debug(f"generate data {str(label)}")
        idx_lst = list(dataframe.iloc[label_indices[label]].index)
        datasets.append({
            "label": label,
            "count": len(idx_lst),
            "property_ids": idx_lst,
        })
    return datasets

        