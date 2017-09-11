import base64
from flask import Flask
from flask_login import current_user
from UHE.admin.views import configure_admin
from UHE.calendar.api import events
from UHE.comment.api import comments
from UHE.extensions import (admin, allows, babel, cache, celery, db,
                            login_manager, mail, plugin_manager, redis_store,
                            captcha_solver)
from UHE.feed.api import feeds
from UHE.index import index
from UHE.message.api import conversations
from UHE.models import Plugin
from UHE.upload import upload
from UHE.user.api import users
from UHE.user.models import User
from UHE.publication.api import publications
from UHE.time.api import time
from UHE.link.api import links

def create_app(config=None):
    app = Flask("UHE", instance_relative_config=True)
    configure_app(app, config)
    # connect(**app.config['MONGODB_SETTINGS'])
    app.signals = {}
    app.update_func = {}
    app.client = {}
    configure_celery_app(app, celery)
    configure_extensions(app)
    configure_admin(app)
    configure_blueprints(app)
    configure_plugins(app)
    configure_manger_accounts(app)
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


def configure_app(app, config):
    app.config.from_object('UHE.config.DevelopmentConfig')
    app.config.from_pyfile('config.py', silent=True)
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


def configure_blueprints(app):
    app.register_blueprint(time, url_prefix='/time')
    app.register_blueprint(publications, url_prefix='/publications')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(conversations, url_prefix='/conversations')
    app.register_blueprint(upload, url_prefix='/upload')
    app.register_blueprint(feeds, url_prefix='/feeds')
    app.register_blueprint(events, url_prefix='/events')
    app.register_blueprint(index, url_prefix='/index')
    app.register_blueprint(comments, url_prefix='/comments')
    app.register_blueprint(links, url_prefix='/link')
    # print(app.url_map)
    # pass


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
    cache.init_app(app)

    # Flask-And-Redis
    redis_store.init_app(app)

    # Flask-Limiter
    # limiter.init_app(app)

    # Flask-Allows
    allows.init_app(app)
    allows.identity_loader(lambda: current_user)
    login_manager.init_app(app)
    # Flask-Plugins
    plugin_manager.init_app(app)

    # @login_manager.request_loader
    # def load_user_from_request(request):
    #     token = request.args.get('token')
    #     if token:
    #         card_id = redis_store.get('token_' + token, '0')
    #         user = User.objects(card_id=card_id).first()
    #         if user:
    #             return user
    #     token = request.headers.get('Authorization')
    #     # print('token',token)
    #     if token:
    #         token = token.replace('Basic ', '', 1)
    #         try:
    #             token = base64.b64decode(token)
    #             print(token)
    #         except TypeError:
    #             pass
    #         card_id = redis_store.get('token_' + token, '0')
    #         user = User.objects(card_id=card_id).first()
    #         if user:
    #             return user
    #     # finally, return None if both methods did not login the user
    #     return None

    @login_manager.user_loader
    def load_user(card_id):
        return User.objects(card_id=card_id).first()
