from typing import Annotated
from fastapi import APIRouter, Request, Path
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import pandas as pd

from app.core.clustering import clustering
from app.core.dataprocessing import read_all_data_from_db, format_reponse_body
from app.models.data import ClusterRequestBody
from app.utils.database import get_db
from app.models.repos_orms import Properties

router = APIRouter(
    prefix="/ml",
    tags=["ml"],
)


@router.post("/clustering/{repo_id}")
async def _clustering(
    repo_id: Annotated[str, Path(title="The ID of the repos to delete")],
    request_body: ClusterRequestBody,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    聚类分析
    Response:
        'code': 类别标签,
        'count': 类别中样本,
        'Formula': 类别中的样本集合,
    """
    # 从数据库读取数据
    properties = await read_all_data_from_db(db=db)
    property_dfs = []
    for property in properties:
        if hasattr(property, 'as_dict'):
            property_dict = property.as_dict()
        else:
            # 否则，使用 property.__dict__ 并排除以 '_' 开头的键
            property_dict = {k: v for k, v in property.__dict__.items() if not k.startswith('_')}
        property_dfs.append(pd.DataFrame([property_dict], index=["Id"]))
    df = pd.concat(property_dfs)
    df = df.set_index("Id")
    # 聚类分析
    cluster_res, model_path = await clustering(
        data=df, 
        repo_id=repo_id, 
        options=request_body.options, 
        func_name=request_body.function
    )
    datasets = await format_reponse_body(cluster_res=cluster_res, dataframe=df)
    # 返回聚类结果
    return datasets
