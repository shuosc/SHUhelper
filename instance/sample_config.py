from datetime import timedelta
# from celery.schedules import crontab
SECRET_KEY = ''
MAIL_SERVER = ''
MAIL_PORT = 465
# MAIL_USE_TLS : default False
MAIL_USE_SSL = True
# MAIL_DEBUG : default app.debug
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ('xxx', 'xxx@xxx.cn')
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
MONGODB_SETTINGS = {
    'db': 'dbname',
    'host': 'localhost,
    'port': 27017
}
REDIS_URL = "redis://localhost:6379/0"
BABEL_DEFAULT_LOCALE = 'zh_CN'
DEFAULT_LOCALE = 'zh_CN'
CAPTCHA_SOLVER_USERNAME = ''
CAPTCHA_SOLVER_PASSWORD = ''
CAPTCHA_SOLVER_SOFTID = 
CAPTCHA_SOLVER_SOFTKEY = ''
TESTING_CARD_ID = ''
TESTING_PASSWORD = ''
TESTING_EMAIL = 'xxx@qq.com'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Shanghai' 
QINIU_ACCESS_KEY = ''
QINIU_SECRET_KEY = ''