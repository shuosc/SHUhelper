from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask_login import UserMixin
from SHUhelper import app
from SHUhelper.config import login_manager

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.String(50))
    username = db.Column(db.String(20))
    comment = db.Column(db.String(240))
    time = db.Column(db.DateTime, default=datetime.now())
    def __repr__(self):
        return '<User %r>' % self.username

class User(UserMixin, db.Model):
    """目前没加散列值处理密码"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer)
    def verify_password(self, password):
        return self.password_hash == password

class Words(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    content_from = db.Column(db.String(200))
    visible = db.Column(db.Boolean, default=True)
    time = db.Column(db.DateTime, default=datetime.now())

class Courses(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    content_from = db.Column(db.String(200))
    visible = db.Column(db.Boolean, default=True)
    time = db.Column(db.DateTime, default=datetime.now())