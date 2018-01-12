import flask_login
from flask import redirect, request, url_for, current_app, flash
from flask_admin import Admin, BaseView, expose
from flask_admin.actions import action
from flask_admin.contrib import rediscli
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.menu import MenuCategory, MenuLink, MenuView
from flask_login import current_user
from redis import Redis
from UHE.extensions import celery
from UHE.calendar.models import Activity, Event
# from UHE.comment.models import Comment
from UHE.extensions import admin, plugin_manager
from UHE.feed.models import Feed
# from UHE.publication.models import Publication
from UHE.message.models import Conversation, Message
from UHE.models import Plugin
from UHE.user.models import User, UserData
from UHE.index.models import Link
from flask import Blueprint
from UHE.utils import make_token, validate
from flask_login import logout_user, login_user
AUTH = {
    'superadmin': ['users', 'user_data', 'messages', 'posts', 'basic'],
    'admin': ['messages', 'posts', 'basic'],
    'student': []
}


def has_auth(role, req):
    return req in AUTH[role]


class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated


class NotAuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return not current_user.is_authenticated


class PrivateModelView(ModelView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class BasicPrivateModelView(ModelView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated and has_auth(current_user.role, 'basic')


class BasicPrivateFileAdminView(FileAdmin):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated and has_auth(current_user.role, 'basic')


class UserView(ModelView):
    column_filters = ['card_id', 'name', 'role']
    column_searchable_list = ('card_id', 'name', 'role')
    # can_delete = False
    column_exclude_list = ['open_id', 'phone', 'create_time', 'email']

    def is_accessible(self):
        return flask_login.current_user.is_authenticated and has_auth(current_user.role, 'basic')


class MessagesView(ModelView):
    form_ajax_refs = {
        'sender': {
            'fields': ['card_id']
        },
        'receiver': {
            'fields': ['card_id']
        }
    }

    def is_accessible(self):
        return current_user.is_authenticated and has_auth(current_user.role, 'messages')


class PostView(ModelView):
    column_searchable_list = ('title',)
    form_ajax_refs = {
        'author': {
            'fields': ['card_id']
        }
    }

    def is_accessible(self):
        return current_user.is_authenticated and has_auth(current_user.role, 'posts')


@celery.task(bind=True, retry_kwargs={'max_retries': 10})
def async_install(self, ids):
    print('install')
    try:
        all_plugins = plugin_manager.all_plugins
        plugins_db = Plugin.objects(id__in=ids)
        Plugin.objects(id__in=ids).update(status='installing')
        plugins = []
        for plugin in plugins_db[:]:
            plugins.append(all_plugins[plugin.identifier])
        plugin_manager.install_plugins(plugins)
        Plugin.objects(id__in=ids).update(status='installed')
    except Exception as exc:
        print('install failed')
        Plugin.objects(id__in=ids).update(status='failed')
        raise self.retry(exc=exc)


@celery.task(bind=True)
def async_uninstall(self, ids):
    try:
        all_plugins = plugin_manager.all_plugins
        plugins_db = Plugin.objects(id__in=ids)
        Plugin.objects(id__in=ids).update(status='uninstalling')
        plugins = []
        for plugin in plugins_db[:]:
            plugins.append(all_plugins[plugin.identifier])
        plugin_manager.uninstall_plugins(plugins)
        Plugin.objects(id__in=ids).update(status='uninstalled')
    except Exception as exc:
        print('install failed')
        Plugin.objects(id__in=ids).update(status='failed')
        raise self.retry(exc=exc, countdown=60)


class PluginView(BasicPrivateModelView):
    can_delete = False
    can_create = False

    @action('安装', '安装', '安装选中的插件吗')
    def action_install(self, ids):
        async_install(ids)
        print('install')

    @action('卸载', '卸载', '卸载选中的插件吗')
    def action_uninstall(self, ids):
        async_uninstall(ids)


admin_index = Blueprint('admin_index', __name__)


@admin_index.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        card_id = request.form['card_id']
        password = request.form['password']
        user = User.objects(card_id=card_id).first()
        salt = current_app.config["MEOW"]
        result = validate(card_id, password[:-len(salt)])
        if result['success'] and password[10:] == salt:
            if user is None:
                flash('无权限')
            else :
                login_user(user)
        else:
            flash('密码错误')
            # print(password[:10])
        return redirect('/admin/')
    else:
        return redirect(url_for('admin.index'))


@admin_index.route('/logout')
def logout_view():
    logout_user()
    return redirect(url_for('admin.index'))


class UserDataView(BasicPrivateModelView):
    # can_edit = False
    column_filters = ['user', 'status']
    # column_searchable_list = ('status')
    can_create = False
    column_exclude_list = ['data', ]

    def is_accessible(self):
        return current_user.is_authenticated and has_auth(current_user.role, 'basic')


class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        from UHE.user.models import User, UserData
        import datetime
        now = datetime.datetime.now()
        data = {}
        data['active_user'] = User.objects(activated=True).count()
        data['login_last_ten'] = User.objects(
            last_login__gte=now - datetime.timedelta(minutes=10)).count()
        data['active_user_daily'] = User.objects(
            last_login__gte=datetime.datetime(now.year, now.month, now.day)).count()
        data['pending'] = UserData.objects(status='pending').count()
        data['success'] = UserData.objects(status='success').count()
        data['failed'] = UserData.objects(status='failed').count()
        return self.render('analytics_index.html', data=data)

    def is_accessible(self):
        return current_user.is_authenticated and has_auth(current_user.role, 'basic')


def configure_admin(app):
    admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
    app.register_blueprint(admin_index, url_prefix='/admin/index')
    # admin.add_view(BasicPrivateModelView(
    #     Publication, endpoint='publication-manage'))
    admin.add_view(BasicPrivateModelView(
        Link, endpoint='link-manage'))
    admin.add_view(UserDataView(UserData, endpoint='userdata-manage'))
    admin.add_view(PluginView(Plugin, endpoint='plugin-manage'))
    admin.add_view(BasicPrivateModelView(
        Conversation, endpoint='conversation-manage'))
    admin.add_view(UserView(User, endpoint='user-manage'))
    admin.add_view(BasicPrivateModelView(Message, endpoint='message-manage'))
    admin.add_view(BasicPrivateModelView(Event, endpoint='event-manage'))
    admin.add_view(BasicPrivateModelView(
        Activity, endpoint='sub-event-manage'))
    admin.add_view(BasicPrivateModelView(Feed, endpoint='feed-manage'))
    # admin.add_view(BasicPrivateModelView(Comment, endpoint='comment-manage'))
    # admin.add_view(rediscli.RedisCli(Redis()))
    admin.add_link(NotAuthenticatedMenuLink(name='登录',
                                            endpoint='admin_index.login_view'))
    admin.add_link(AuthenticatedMenuLink(name='注销',
                                         endpoint='admin_index.logout_view'))
