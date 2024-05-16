import os
import logging
import inspect
from functools import wraps

from app.config import app_conf


class BingoLogger:

    def __init__(self, name, level=logging.DEBUG, file_name=None):
        if not os.path.exists(app_conf.ROOT_PATH):
            os.makedirs(app_conf.ROOT_PATH)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        if file_name:
            file_handler = logging.FileHandler(file_name)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)


# 创建全局 logger 对象
logger = BingoLogger(name=app_conf.APP_NAME,
                    level=app_conf.LEVEL,
                    file_name=app_conf.LOG_PATH)


# 打印参数的装饰器
def show_args(func):
    # 使用 functools.wraps 保持原始函数的元数据
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.logger.debug("Show Arguments: ")
        # 打印出所有参数的名称和值
        args_spec = inspect.getfullargspec(func)
        all_args = kwargs.copy()
        all_args.update({arg: arg_value for arg, arg_value in zip(args_spec.args, args)})
        bound_arguments = inspect.signature(func).bind(**all_args)
        bound_arguments.apply_defaults()
        arguments = bound_arguments.arguments
        for arg_name, arg_value in arguments.items():
            logger.logger.debug(f"{arg_name}: {arg_value}")
        # 调用原始函数
        return func(*args, **kwargs)
    return wrapper
