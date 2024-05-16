"""
使用pydantic进行类别映射
"""
from pydantic import BaseModel


class UserMixin(BaseModel):
    creator: str | None = None


class ClusterOptions(BaseModel):
    # DBSCAN
    eps: float = 0.5
    min_samples: int = 10
    dosage: bool = True


class ClusterRequestBody(UserMixin):
    function: str = "DBSCAN"
    options: ClusterOptions | None = None