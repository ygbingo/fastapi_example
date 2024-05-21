from pydantic_settings import BaseSettings


class FastApiConf(BaseSettings):
    APP_NAME: str = "AIBingo"
    LEVEL: str = "INFO"
    LOGGER_SHOW_LEN: int = 1000
    ROOT_PATH: str = "ai-bingo"  # 与docker-compose的挂载路径一致
    LOG_PATH: str = "ai-bingo/app.log"

    APP_VERSION: str = "0.2.0"

app_conf = FastApiConf()


class MLConf(BaseSettings):
    USE_NORMALIZED: int = 1
    MODEL_PATH: str = "ai-bingo/models/"

    # bayesian-opt
    N_CALLS: int = 5
    N_INITIAL_POINTS: int = 5
    N_JOBS: int = 1

    # 输出的精度
    decimal_places: int = 4

ml_conf = MLConf()


class DBConf(BaseSettings):
    # local
    DB_USERNAME: str = "postgres"
    DB_SECRET: str = "a"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "plm"

    enabled: bool = True


db_conf = DBConf()