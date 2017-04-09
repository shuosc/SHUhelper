import os.path as op
from models import *
from api import admin, admin
from flask_mongoengine import MongoEngine
from flask_admin.contrib.mongoengine import ModelView
from flask_admin import Admin


class UserView(ModelView):
    column_filters = ['card_id']
    column_searchable_list = ('card_id',)

class MessagesView(ModelView):
    form_ajax_refs = {
        'sender': {
            'fields': ['card_id']
        },
        'receiver':{
            'fields': ['card_id']
        }
    }


