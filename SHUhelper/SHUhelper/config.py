'''
cofig there
'''
import os
from SHUhelper import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import MemcachedCache
from werkzeug.contrib.cache import SimpleCache
from flask_login import LoginManager
from flask_script import Manager
CACHE = MemcachedCache(['127.0.0.1:11211'])
from flask import Flask
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'course.db'),
                       DEBUG=False,
                       SECRET_KEY='shuhelper',
                       USERNAME='admin',
                       PASSWORD='default'))
app.secret_key = u'key'
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
manager = Manager(app)
#class DevlopmentConfig(Config):
#    DEBUG = True;
#    CACHE = SimpleCache()

#class ProductionConfig(Config):
#    CACHE = MemcachedCache(['127.0.0.1:11211'])

#class TesingConfig(Config):
#    pass

#config = {
#    'development' : DevlopmentConfig,
#    'tesing' : TesingConfig,
#    'prooduction' : ProductionConfig,
#    'default' : DevlopmentConfig
#    }

