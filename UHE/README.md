
#### 创建python虚拟环境


### windows 

`bash`
`virtualenv env`
`source env/bin/activate`
`pip install -r requirements.txt`
`pip install e .`
`make run`


#### 设置环境变量

#### 启动redis，mongoDB服务器

#### 启动Celery Broker

`celery -A celery_worker.celery worker --beat --loglevel=info`

#### 运行测试服务器

 gunicorn -w 10 --reload -D -b 127.0.0.1:4001 api:app
