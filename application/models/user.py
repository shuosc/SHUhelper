from Crypto.Cipher import AES
from flask import abort, request, current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from application.services.sim_clients import Services
from application.extensions import db, celery, login_manager, redis_store
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import uuid
import binascii
from application.utils import CRUDMixin
# from sqlalchemy.dialects.postgresql import UUID
class User(UserMixin, db.Model,CRUDMixin):
    id = db.Column(db.String(), primary_key=True)
    # uuid = Column(UUID, unique=True, nullable=False)
    open_id = db.Column(db.String())
    name = db.Column(db.String())
    username = db.Column(db.String(80), unique=True, nullable=False)
    nickname = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    avatar_URL = db.Column(db.String(),default='avatar_default.jpg')
    creat_time = db.Column(db.DateTime, nullable=False,
        default=datetime.now)
    last_login = db.Column(db.DateTime, nullable=False,
        default=datetime.now)
    activated = db.Column(db.Boolean)
    robot = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)
    pw_hash = db.Column(db.String())
    oauth = db.relationship('SocialOAuth', lazy='select',
                            backref=db.backref('user', lazy=True))

    def authenticate(self, password):
        if check_password_hash(self.pw_hash, password):
            return True
        else:
            return False

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def regisiter(self, password):
        client = Services(self.id, password)
        if client.login() and client.get_data():
            self.name = client.data['name']
            self.username = client.data['nickname']
            self.pw_hash = generate_password_hash(password)
            self.save()
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.name + str(self.id)

    def to_dict_public(self):
        return {
            'avatarURL': self.avatar_URL,
            'id': self.id,
            'name': self.nickname
        }

    @property
    def display_name(self):
        return self.name

    def to_dict(self):
        result = {
            'id': self.id,
            'avatarURL': self.avatar_URL,
            'name': self.name,
            'nickname': self.nickname,
            'email': self.email,
            'lastLogin': str(self.last_login)
        }
        return result

    def login(self, token):
        self.last_login = datetime.now()
        self.save()
        result = {
            'avatarURL': self.avatar_URL,
            'token': token,
            'name': self.name,
            'nickname': self.nickname
        }
        return result

class SocialOAuth(db.Model,CRUDMixin):
    id = db.Column(db.UUID(as_uuid=True),default=uuid.uuid4, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    source = db.Column(db.String())
    site = db.Column(db.String())
    site_uid = db.Column(db.String())
    site_uname = db.Column(db.String())
    created_time = db.Column(db.DateTime)
    unionid = db.Column(db.String())
    open_id = db.Column(db.String())
    access_token = db.Column(db.String())
    refresh_token = db.Column(db.String())
    expire_date = db.Column(db.DateTime)


class UserData(db.Model,CRUDMixin):
    """
    collection of user data, from query used as cache, data encrpted with aes
    """
    id = db.Column(db.UUID(as_uuid=True),default=uuid.uuid4, primary_key=True)
    data = db.Column(db.String())
    name = db.Column(db.String())
    user = db.Column(db.String, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime)
    status = db.Column(db.String())
    # client_id = StringField(default='client_')

    def get_client(self):
        client = redis_store.get(user_data.client_id, None)
        return client

    def lock_save(self, pw):
        in_len = len(self.data)
        pad_size = 16 - (in_len % 16)
        self.data = self.data.ljust(in_len + pad_size, chr(pad_size))
        if len(pw) < 16:
            pw += '0' * (16 - len(pw))
        iv = binascii.a2b_hex('000102030405060708090a0b0c0d0e0f')
        obj = AES.new(pw, AES.MODE_CBC, iv)
        self.data = str(binascii.b2a_base64(obj.encrypt(self.data)))[2:-2]
        self.save()


# @celery.task()
# def update_user_data(user_data_id):
#     user_data = UserData.objects(_id=user_data_id).first()
#     client = user_data.get_client()
#     client.update()
#     redis_store.set(user_data.client_id, client)


@login_manager.request_loader
def request_loader(request):
    token = request.headers.get('Authorization')
    if token:
        token = token.replace('Bearer ', '', 1)
        user = User.verify_auth_token(token)
        if user:
            return user
    return None


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)
