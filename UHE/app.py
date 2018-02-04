
from flask import Flask
from flask_login import current_user

from UHE.admin.views import configure_admin
from UHE.calendar.api import events
from UHE.calendar.time import Time
# from UHE.comment.api import comments
from UHE.extensions import (admin, allows, babel, cache, celery, db,
                            login_manager, mail, plugin_manager, redis_store, oauth,
                            captcha_solver)
from UHE.feed.api import feeds
from UHE.index.api import index
from UHE.message.api import conversations
from UHE.models import Plugin
from UHE.user.api import users
from UHE.user.models import User
from mockredis import MockRedis
from flask_redis import FlaskRedis
from UHE.signals import app_start


def create_app(config=None):
    """
    app factory, return an configured instance 
    """
    app = Flask("UHE", instance_relative_config=True)
    configure_app(app, config)
    # connect(**app.config['MONGODB_SETTINGS'])
    # app.signals = {}
    # app.update_func = {}
    # app.client = {}
    configure_celery_app(app, celery)
    configure_extensions(app)
    configure_admin(app)
    configure_blueprints(app)
    configure_plugins(app)
    configure_manger_accounts(app)
    # signal
    app_start.send(app)
    # configure_tasks(app,celery)
    return app


def create_celery_app(config=None):
    app = Flask("UHE", instance_relative_config=True)
    configure_app(app, config)
    app.signals = {}
    app.update_func = {}
    configure_extensions(app)
    configure_admin(app)
    configure_blueprints(app)
    configure_celery_app(app, celery)
    # configure_tasks(app,celery)
    return app


def configure_manger_accounts(app):
    # [todo] configure super admin
    plugins = Plugin.objects()
    for plugin in plugins:
        user = User.objects(card_id=plugin.identifier).first()
        if user is None:
            user = User(card_id=plugin.identifier,
                        name=plugin.identifier, activated=True, robot=True)
            user.save()
    user = User.objects(card_id='00000001').first()
    if user is None:
        user = User(card_id='00000001',
                    name='匿名用户', activated=True, robot=True)
        user.save()


def configure_app(app, config):
    # app.config.from_object('UHE.config.DevelopmentConfig')
    app.config.from_pyfile('config.py')
    # try to update the config via the environment variable
    # Parse the env for UHE_ prefixed env variables and set
    # them on the config object
    # app_config_from_env(app, prefix="UHE_")


def configure_plugins(app):
    plugins = plugin_manager.all_plugins
    plugins_db = Plugin.objects()
    for plugin in plugins.values():
        plugin_db = Plugin.objects(identifier=plugin.identifier).first()
        if plugin_db is None:
            plugin_db = Plugin(
                name=plugin.name, identifier=plugin.identifier, enable=True)
            plugin_db.save()
    for plugin in plugins_db[:]:
        if plugin.identifier not in plugins.keys():
            plugin.delete()


def configure_celery_app(app, celery):
    """Configures the celery app."""
    app.config.update({'BROKER_URL': app.config["CELERY_BROKER_URL"]})
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


# def register_blueprints(app):
#     for name in find_modules('flaskr.blueprints'):
#         mod = import_string(name)
#         if hasattr(mod, 'bp'):
#             app.register_blueprint(mod.bp)
#     return None

def configure_blueprints(app):
    app.register_blueprint(index, url_prefix='')
    # app.register_blueprint(time, url_prefix='/time')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(conversations, url_prefix='/conversations')
    # app.register_blueprint(upload, url_prefix='/upload')
    app.register_blueprint(feeds, url_prefix='/feeds')
    app.register_blueprint(events, url_prefix='/events')
    # app.register_blueprint(comments, url_prefix='/comments')
    # print(app.url_map)
    # pass


# def register_cli(app):
#     """[todo]""""
#     @app.cli.command('initdb')
#     def initdb_command():
#         """Creates the database tables."""
#         print('Initialized the database.')

def configure_extensions(app):
    """Configures the extensions."""
    # Flask-BabelEx
    babel.init_app(app)

    # Captcha Solver
    captcha_solver.init_app(app)

    # Flask-Mail
    mail.init_app(app)

    # Flask-Admin
    admin.init_app(app)

    # Flask-Mongo Engine
    db.init_app(app)

    # Flask-Cache
    cache.init_app(app, config={'CACHE_TYPE': 'redis', 'CACHE_KEY_PREFIX': 'UHE',
                                'CACHE_REDIS_URL': app.config['REDIS_URL']})

    print(app.testing)
    # Flask-And-Redis

    redis_store.init_app(app)

    # Flask-Limiter
    # limiter.init_app(app)

    # Flask-Allows
    allows.init_app(app)
    allows.identity_loader(lambda: current_user)
    login_manager.init_app(app)
    # Flask-Plugins
    app.school_time = Time()

    oauth.init_app(app)

    plugin_manager.init_app(app)
