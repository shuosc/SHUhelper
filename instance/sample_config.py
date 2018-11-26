
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


# babel locale configs
BABEL_DEFAULT_LOCALE = 'zh_CN'
DEFAULT_LOCALE = 'zh_CN'


# === these settings are not required

# celery broker settings, check celery docs to confirm
CELERY_BROKER_URL = ''
CELERY_RESULT_BACKEND = ''

# captcha solver for SHU sites
# leave it empty if you don't have one
CAPTCHA_SERVER = ''

# fill with your own cardID and password here
TESTING_CARD_ID = ''
TESTING_PASSWORD = ''

# write down your email
TESTING_EMAIL = ''

# qiniu access key and secret key, see qiniu.com to apply one
# leave it empty if you don't need to
QINIU_ACCESS_KEY = ''
QINIU_SECRET_KEY = ''

# leave it empty if you don't know
PROXY = '' 
MEOW = "123"