import datetime

from Crypto.Cipher import AES
from flask import abort,request
from flask_login import UserMixin
from mongoengine import (BooleanField, DateTimeField, EmailField, ReferenceField, StringField)
from werkzeug.security import check_password_hash, generate_password_hash
from UHE.plugins.SHU_api.client import Services
from UHE.extensions import db, celery,login_manager,redis_store


class User(UserMixin, db.Document):
    card_id = StringField(primary_key=True,unique=True)
    open_id = StringField(default='')
    name = StringField(default="未激活")
    username = StringField(default="")
    nickname = StringField(default="未激活用户")
    email = EmailField()
    role = StringField(default="student")
    avatar = StringField(default='avatar_default.jpg')
    creat_time = DateTimeField(default=datetime.datetime.now)
    last_login = DateTimeField(default=datetime.datetime.now)
    activated = BooleanField(default=False)
    robot = BooleanField(default=False)
    deleted = BooleanField(default=False)
    hash = StringField(default='')
    custom = StringField(default='{}')
    meta = {'strict': False}

    def authenticate(self, password):
        if check_password_hash(self.hash, password):
            return True
        else:
            return False

    def regisiter(self, password):
        client = Services(self.card_id, password)
        if client.login() and client.get_data():
            self.name = client.data['name']
            self.nickname = client.data['nickname']
            self.hash = generate_password_hash(password)
            self.save()
            # self.reload()
            return True
        else:
            return False

    def get_id(self):
        return self.card_id

    def __unicode__(self):
        return self.name + str(self.card_id)

    def to_dict_public(self):
        return {
            'avatar': self.avatar,
            'cardID': self.card_id,
            'name': self.nickname
        }

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

    def login(self, token):
        self.last_login = datetime.datetime.now()
        self.save()
        result={
            'avatar': self.avatar,
            'token': token,
            'name': self.name,
            'nickname': self.nickname,
            'custom': self.custom
        }
        return result


class UserData(db.Document):
    """
    collection of user data, from query used as cache, data encrpted with aes
    """
    data = StringField()
    identifier = StringField(unique_with='user')
    user = ReferenceField(User)
    last_modified = DateTimeField(default=datetime.datetime.now)
    need_update = BooleanField(default=False)
    status = StringField()
    client_id = StringField(default='client_')
    meta = {'strict': False}

    def get_client(self):
        client = redis_store.get(user_data.client_id, None)
        return client

    def lock_save(self, pw):
        import binascii
        in_len = len(self.data)
        pad_size = 16 - (in_len % 16)
        # print(self.data )
        self.data = self.data.ljust(in_len + pad_size, chr(pad_size))
        # print(self.data )
        if len(pw) < 16:
            pw += '0' * (16 - len(pw))
        iv = binascii.a2b_hex('000102030405060708090a0b0c0d0e0f')
        obj = AES.new(pw, AES.MODE_CBC, iv)
        # print(self.data)
        self.data = str(binascii.b2a_base64(obj.encrypt(self.data)))[2:-2]
        # print(self.data)
        self.save()


@celery.task()
def update_user_data(user_data_id):
    user_data = UserData.objects(_id=user_data_id).first()
    client = user_data.get_client()
    client.update()
    redis_store.set(user_data.client_id, client)

@login_manager.request_loader
def request_loader(request):
    # print(request)
    # token = request.args.get('token')
    # print('request')
    # print(token)
    # if token:
    #     card_id = redis_store.get('token_' + token, '0')
    #     user = User.objects(card_id=card_id).first()
    #     if user:
    #         return user
    token = request.headers.get('Authorization')
    if token:
        token = token.replace('Basic ', '', 1)
        try:
            token = base64.b64decode(token)
            print(token)
        except TypeError:
            pass
        card_id = redis_store.get('token_' + token, '0')
        user = User.objects(card_id=card_id).first()
        if user:
            return user
    # finally, return None if both methods did not login the user
    return None

@login_manager.user_loader
def user_loader(card_id):
    return User.objects(card_id=card_id).first()
