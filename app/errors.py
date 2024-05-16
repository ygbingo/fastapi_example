from fastapi import HTTPException


# 找不到资源, 400~499
class SupportError(HTTPException):
    def __init__(self, func_name=None) -> None:
        super().__init__(status_code=405, detail=f"This method({func_name}) is not supported yet")
    

class GetModelException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="The model file is missing, please re-cluster")


class GetRepoException(HTTPException):
    def __init__(self, repo_id=None) -> None:
        super().__init__(status_code=404, detail=f"Project {repo_id} does not exist!")


class GetLabelException(HTTPException):
    def __init__(self, repo_id=None, label=None) -> None:
        super().__init__(status_code=404, detail=f"Category does not exist, check project ID ({repo_id}) and category number ({label})")


# 内部错误, 500~599
class TrainNotDone(HTTPException):
    def __init__(self, repo_id=None, label=None) -> None:
        super().__init__(status_code=503, detail=f"Please train first: {label} category of {repo_id}, or wait for training to complete")


class SamplesTooSmall(HTTPException):
    def __init__(self, samples_cnt=None) -> None:
        super().__init__(status_code=503, detail=f"Training failed, the number of samples ({samples_cnt}) is too small")


class TrainErrorWithoutQuota(HTTPException):
    def __init__(self, repo_id=None, label=None) -> None:
        super().__init__(status_code=503, detail=f"Training failed without quotas repo: {repo_id} label: {label}")