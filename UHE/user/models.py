import datetime

from flask import abort
from flask_login import UserMixin
from mongoengine import (BooleanField, DateTimeField, EmailField,ReferenceField,
                         StringField)

from UHE.client import Services
from UHE.extensions import db,celery

class User(UserMixin, db.Document):
    card_id = StringField()
    open_id = StringField()
    name = StringField(default="未激活")
    username = StringField()
    nickname = StringField()
    email = EmailField()
    role = StringField()
    avatar = StringField(default='avatar_default.jpg')
    creat_time = DateTimeField(default=datetime.datetime.now)
    last_login = DateTimeField(default=datetime.datetime.now)
    activated = BooleanField(default=False)
    robot = BooleanField(default=False)
    deleted = BooleanField(default=False)
    meta = {'strict': False}

    def get_id(self):
        return self.card_id

    def __unicode__(self):
        return self.name + self.card_id

    # def to_dict(self):
    #     return {"card_id": self.card_id, "name": self.name, "nickname": self.nickname}

    def validate_password(self, password):
        client = Services(self.card_id, password)
        if client.login() and client.get_data():
            result = {
                'name': client.data['name'],
                'card_id': self.card_id
            }
        else:
            abort(401)
        return result

    @property
    def display_name(self):
        return self.name

    def to_dict(self):
        result = {
            'cardID': self.card_id,
            'avatar': self.avatar,
            'name': self.name,
            'nickname': self.nickname,
            'email': self.email,
            'lastLogin': str(self.last_login)
        }
        return result


class UserData(db.Document):
    """
    collection of user data, from query used as cache, data encrpted with aes
    """
    data = StringField(default='')
    identifier = StringField()
    user = ReferenceField(User)
    last_modified = DateTimeField(default=datetime.datetime.now)
    need_update = BooleanField()
    status = StringField()
    client_id = StringField(default='client_')

    def get_client(self):
        client = redis_store.get(user_data.client_id,None)
        return client

@celery.task()
def update_user_data(user_data_id):
    user_data = UserData.objects(_id=user_data_id).first()
    client = user_data.get_client()
    client.update()
    redis_store.set(user_data.client_id, client)
