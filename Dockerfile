FROM python:3.12
WORKDIR /src

COPY ./app /src/app
COPY requirements.txt /src

# 运行命令
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 运行服务
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]