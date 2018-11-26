import binascii
import uuid
from datetime import datetime

from Crypto.Cipher import AES
from flask import abort, current_app, request
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from marshmallow import post_load
from werkzeug.security import check_password_hash, generate_password_hash

from application.extensions import celery, db, login_manager, ma, redis_store
from application.services.sim_clients import Services
from application.utils import CRUDMixin, TimeMixin

# from sqlalchemy.dialects.postgresql import UUID
# from application.models.teaching_manage import StudentClass


class SocialOAuth(db.Model, CRUDMixin, TimeMixin):
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    session_key = db.Column(db.String())
    source = db.Column(db.String())
    site = db.Column(db.String())
    site_uid = db.Column(db.String())
    site_uname = db.Column(db.String())
    unionid = db.Column(db.String())
    open_id = db.Column(db.String())
    access_token = db.Column(db.String())
    refresh_token = db.Column(db.String())
    expire_date = db.Column(db.DateTime)

    def bind_user(self, user_id):
        self.user_id = user_id
        self.save()


class User(UserMixin, db.Model, CRUDMixin, TimeMixin):
    id = db.Column(db.String(), primary_key=True)
    open_id = db.Column(db.String())
    name = db.Column(db.String(), index=True)
    username = db.Column(db.String(80))
    nickname = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    avatar_URL = db.Column(db.String(), default='avatar_default.jpg')
    last_login = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)
    activated = db.Column(db.Boolean)
    robot = db.Column(db.Boolean)
    pw_hash = db.Column(db.String())
    oauth = db.relationship('SocialOAuth', lazy='select',
                            backref=db.backref('user', lazy=True))
    user_type = db.Column(db.String, default='user')
    extra = db.Column(db.JSON)
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

    @staticmethod
    def is_teacher_id(user_id):
        return user_id.startswith("100") or user_id.startswith("510") or user_id.startswith("310") or user_id.startswith("610")

    @staticmethod
    def is_student_id(user_id):
        return user_id[2:4] == '12' or user_id[2:4] == '17':

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
            'lastLogin': str(self.last_login),
            'username': self.username
        }
        return result

    def login(self, token):
        self.last_login = datetime.now()
        self.save()
        result = {
            'avatarURL': 'https://static.shuhelper.cn/' + self.avatar_URL,
            'token': token,
            'name': self.name,
            'nickname': self.nickname,
            'userID': self.id,
            'username': self.username
        }
        return result


# student_classes = db.Table('student_class',
#                            db.Column('student_id', db.String, db.ForeignKey(
#                                'undergraduate_student.id'), primary_key=True),
#                            db.Column('class_id', db.UUID(as_uuid=True), db.ForeignKey(
#                                'class.id'), primary_key=True),
#                            db.Column('grade_1', db.Integer),
#                            db.Column('grade_2', db.Integer))

class UndergraduateStudent(User):
    id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    # classes = db.relationship('Class', secondary=student_classes, lazy='subquery',
    #    backref=db.backref('dtudents', lazy=True))
    classes = db.relationship('StudentClass', back_populates="student")
    __mapper_args__ = {
        'polymorphic_identity': 'undergraduate_student',
    }

    def __unicode__(self):
        return self.name


class UndergraduateStudentSchema(ma.ModelSchema):
    # oauth = ma.List()
    class Meta:
        model = UndergraduateStudent
        exclude = ('oauth', 'pw_hash')

    @post_load
    def load(self, data):
        return UndergraduateStudent(**data)


undergraduate_student_schema = UndergraduateStudentSchema()
undergraduate_students_schema = UndergraduateStudentSchema(many=True)


class Teacher(User):
    id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)

    # degree = db.Column(db.String())
    # sex = db.Column(db.String())
    # title = db.Column(db.String())
    # education = db.Column(db.String())
    # dept = db.Column(db.String())
    # cs = db.Column(db.String())
    # intro = db.Column(db.String())

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

    def __unicode__(self):
        return self.name


class TeacherSchema(ma.ModelSchema):
    # oauth = ma.List()
    class Meta:
        model = Teacher
        exclude = ('oauth', 'pw_hash')

    @post_load
    def load(self, data):
        return Teacher(**data)


teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)


class GraduateStudent(User):
    id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'graduate_student',
    }

    def __unicode__(self):
        return self.name


class UserData(db.Model, CRUDMixin, TimeMixin):
    """
    collection of user data, from query used as cache, data encrpted with aes
    """
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    data = db.Column(db.String())
    name = db.Column(db.String())
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    status = db.Column(db.String())
    # client_id = StringField(default='client_')

    def to_json(self):
        return {
            'data': self.data,
            'name': self.name,
            'created': self.created,
            'status': self.status
        }

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
