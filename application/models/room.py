from flask import Flask, request, jsonify, current_app
from application.extensions import db
from flask.views import MethodView
from application.models.user import User
from application.enums import Campus
from datetime import datetime
import requests
from sqlalchemy.dialects.postgresql import ENUM
from application.utils import CRUDMixin


class Room(db.Model, CRUDMixin):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String())
    campus = db.Column(db.String())
    building = db.Column(db.String)
    floor = db.Column(db.Integer)
    no = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    name = db.Column(db.String(80), nullable=False)
    detail = db.Column(db.String(80), nullable=False)
    available = db.Column(db.Boolean, default=True)
    orders = db.relationship('Order', lazy='select',
                             backref=db.backref('room', lazy=True))


class Order(db.Model, CRUDMixin):
    __tablename__ = 'room_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    date = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    remark = db.Column(db.String)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    # room = db.relationship('Room',backref=db.backref('orders', lazy=True))

    @property
    def status(self):
        now = datetime.now()
        timedelta = now - self.date
        if timedelta.days > 0:
            return '已结束'
        elif timedelta.days < 0:
            return '未开始'
        elif timedelta.days == 0:
            # course = current_app.school_time.get_course()
            now = datetime.now()
            if self.start_time <= now and now <= self.end_time:
                return '正在进行'
            if now < self.start_time:
                return '未开始'
            if now > self.end_time:
                return '已结束'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'userID': self.user_id,
            'userName': self.user.name,
            'roomID': self.room_id,
            'room': self.room.name,
            'start': self.start_time.timestamp(),
            'end': self.end_time.timestamp(),
            'date': self.date.timestamp(),
            'status': self.status
        }

    @staticmethod
    def from_json(json_post):
        return Order(user_id=json_post['userID'],
                     room_id=json_post['roomID'],
                     date=datetime.fromtimestamp(json_post['date']),
                     start_time=datetime.fromtimestamp(json_post['start']),
                     end_time=datetime.fromtimestamp(json_post['end']))
