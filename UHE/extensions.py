from celery import Celery
from flask_admin import Admin
from flask_allows import Allows
from flask_babelex import Babel
from flask_caching import Cache
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis
from flask import current_app
from UHE.plugins import PluginManager
from UHE.plugins.SHU_captcha import Solver
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_oauthlib.provider import OAuth2Provider
# from UHE.schedule import clock

class AnonymousUser(AnonymousUserMixin):
    id = '00000001'
    def get_id(self):
        return '00000001'

login_manager = LoginManager()
login_manager.anonymous_u00ser = AnonymousUser
mail = Mail()

allows = Allows()

admin = Admin(name='SHUhelper Violet', template_mode='bootstrap3')

cache = Cache()

redis_store = FlaskRedis(decode_responses=True)

db = MongoEngine()

celery = Celery()

plugin_manager = PluginManager()

captcha_solver = Solver()

babel = Babel()

oauth = OAuth2Provider(app)

limiter = Limiter(auto_check=False, key_func=get_remote_address)

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(5.0, clock.dalay('world'), expires=10)

#     # Executes every Monday morning at 7:30 a.m.
#     # sender.add_periodic_task(
#     #     crontab(hour=7, minute=30, day_of_week=1),
#     #     test.s('Happy Mondays!'),
#     # )
