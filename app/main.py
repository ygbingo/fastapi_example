from fastapi import FastAPI

from app.config import app_conf
from app.routers import ml

app = FastAPI(title=app_conf.APP_NAME)

app.include_router(ml.router)