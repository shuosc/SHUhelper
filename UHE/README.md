
#### 创建python虚拟环境

`pip install e .`

`export FLASK_APP=run.py`

`export FLASK_DEBUG=1`

`flask run`
#### 设置环境变量

#### 启动redis，mongoDB服务器

#### 启动Celery Broker

`celery -A celery_worker.celery worker --beat --loglevel=info`

#### 运行测试服务器

 gunicorn -w 10 --reload -D -b 127.0.0.1:4001 api:app
