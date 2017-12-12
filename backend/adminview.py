import flask_login
from flask_login import current_user
from flask import redirect, url_for, request
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.menu import MenuCategory, MenuLink, MenuView

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
    column_filters = ['card_id']
    column_searchable_list = ('card_id',)
    can_delete = False
    column_exclude_list = ['open_id', 'phone', 'create_time', 'email']
    def is_accessible(self):
        return flask_login.current_user.is_authenticated and has_auth(current_user.role, 'users')

class UserDataView(ModelView):
    can_edit = False
    can_create = False
    column_exclude_list = ['data',]
    def is_accessible(self):
        return current_user.is_authenticated and has_auth(current_user.role, 'user_data')


class MessagesView(ModelView):
    form_ajax_refs = {
        'sender': {
            'fields': ['card_id']
        },
        'receiver':{
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
# from flask_admin.contrib.mongoengine import ModelView


# class UserView(ModelView):
#     column_filters = ['card_id']
#     column_searchable_list = ('card_id',)

# class MessagesView(ModelView):
#     form_ajax_refs = {
#         'sender': {
#             'fields': ['card_id']
#         },
#         'receiver':{
#             'fields': ['card_id']
#         }
#     }
