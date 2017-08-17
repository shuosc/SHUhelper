class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True

    #Mail Settings
    MAIL_SERVER = ''
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # MAIL_DEBUG : default app.debug
    MAIL_USERNAME = 'me@example.com'
    MAIL_DEFAULT_SENDER = ('me','me@example.com')
    SECRET_KEY = 'SECRET_KEY'

    #MAIL_USE_TLS : default False
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ('', '')

    #Celery Settings
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'

    #MongoDB Settings
    MONGODB_SETTINGS = {
        'db': 'UHE',
        'host': '127.0.0.1',
        'port': 27017
    }

    # Redis
    REDIS_URL = "redis://localhost:6379/0"

    #Babel
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    
    #RK Captcha Solver Service
    CAPTCHA_SOLVER_USERNAME = ''
    CAPTCHA_SOLVER_PASSWORD = ''
    CAPTCHA_SOLVER_SOFTID = 0
    CAPTCHA_SOLVER_SOFTKEY = ''


class TestingConfig(Config):
    TESTING = True
