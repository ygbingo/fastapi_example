# fastapi_example
基于 fastapi + sqlalchemy + asyncio 实现一个AI后端服务

# 目录
- main.py: 入口
- config.py: 配置信息
- models: 数据结构
- core: 核心代码, 如数据处理、算法类
- routers: api接口
- utils: 工具类, 日志等

# 运行

1. clone代码
2. 安装环境
3. 运行fastapi
```shell
uvicorn app.main:app --reload
```

# 测试
1. 创建数据:
```shell
python scripts/mock_postgres.py
```

2. 发送请求:
```shell
curl --location 'http://127.0.0.1:8000/ml/clustering/0c46960f-f826-4cf8-b4a6-e58af47d631c' --header 'Content-Type: application/json' --data '{"creator": "34eb5596-57b7-4056-a5cd-24eba780132a","options": {"method": "DBSCAN","basis": 0,"eps": "3","min_samples": "20"}}'
```
![request](./imgs/post-request.png)

3. 接收请求
![response](./imgs/post-response.png)



# 很多其他特性在项目里没有展示出来, 小伙伴们可以在Comments里给我留言