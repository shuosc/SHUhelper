
# === these settings are required

# you have to generate an random string     
SECRET_KEY = 'random string'

# mongo db is required
MONGODB_SETTINGS = {
    'host': 'mongodb://localhost:27017/UHE',
}

# redis is required
REDIS_URL = "redis://localhost:6378/0"

MAIL_SERVER = 'mail.sample.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'me@sample.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = ('name', 'me@sample.om')


# these config for babel locale
BABEL_DEFAULT_LOCALE = 'zh_CN'
DEFAULT_LOCALE = 'zh_CN'


# === these settings you can leave it empty

# celery broker settings, check celery docs for confirm
# but you can just leave it empty, beacuse celery was deprecated
CELERY_BROKER_URL = ''
CELERY_RESULT_BACKEND = ''

# captcha solver for SHU sites
# leave it empty if you dont have one
CAPTCHA_SERVER = ''

# write down your cardID and password here
TESTING_CARD_ID = ''
TESTING_PASSWORD = ''

# write down your email
TESTING_EMAIL = ''

# qiniu access key and secret key, see qiniu.com to apply one
# leave it empty if you dont need to
QINIU_ACCESS_KEY = ''
QINIU_SECRET_KEY = ''

# you can leave it empty
PROXY = '' 
MEOW = "123"