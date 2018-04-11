from celery import Celery
from flask_admin import Admin
from flask_allows import Allows
from flask_babelex import Babel
from flask_caching import Cache
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis
from flask import current_app,g
from flask_sqlalchemy import SQLAlchemy
from UHE.plugins import PluginManager
from UHE.plugins.SHU_captcha import Solver
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_oauthlib.provider import OAuth2Provider
from flask.sessions import SecureCookieSessionInterface
from flask_login import current_user, user_loaded_from_request
from sqlalchemy.dialects.postgresql.base import UUID
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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

db = SQLAlchemy()
db.UUID = UUID
celery = Celery()

plugin_manager = PluginManager()

captcha_solver = Solver()

babel = Babel()

oauth = OAuth2Provider()

limiter = Limiter(auto_check=False, key_func=get_remote_address)

class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)

@user_loaded_from_request.connect
def user_loaded_from_request(self, user=None):
    g.login_via_header = True
# jwt = Serializer()
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
