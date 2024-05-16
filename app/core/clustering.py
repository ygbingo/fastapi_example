import pickle
import os
from sklearn.cluster import DBSCAN

from app.models.data import ClusterOptions
from app.utils.ml_utils import (
    normalized
)
from app.utils.logger import logger
from app.config import ml_conf
from app.errors import (
    SamplesTooSmall,
    SupportError
)


def get_clustering_model_path(repo_id):
    model_path = ml_conf.MODEL_PATH.format(repo_id=repo_id)
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    return model_path + "clustering.pkl"


async def clustering(data, repo_id, options: ClusterOptions, func_name="DBSCAN"):
    # 构建聚类模型
    logger.logger.info(f"Start Clustering data shapes: {data.shape} function: {func_name} options: {options}")
    if data.shape[0] < 1 or data.shape[1] < 1:
        raise SamplesTooSmall(str(data.shape))
    model_path = get_clustering_model_path(repo_id)
    match func_name:
        case "DBSCAN":
            df_M_norm = normalized(data)
            cluster_res = DBSCAN(eps=options.eps, min_samples=options.min_samples).fit(df_M_norm)
        case _:
            raise SupportError
    logger.logger.info(f"save model in {model_path}")
    pickle.dump(cluster_res, open(model_path, 'wb'))
    return cluster_res, model_path
