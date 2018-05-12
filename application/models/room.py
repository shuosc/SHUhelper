from flask import Flask, request, jsonify, current_app
from application.extensions import db
from flask.views import MethodView
from application.models.user import User
from application.enums import Campus
from datetime import datetime
import requests
from sqlalchemy.dialects.postgresql import ENUM
from application.utils import CRUDMixin, current_ten_minutes,current_day_seconds
import uuid
class Room(db.Model, CRUDMixin):
    __tablename__ = 'room'
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
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
    __tablename__ = 'room_booking_order'
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    room_id = db.Column(db.UUID, db.ForeignKey('room.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    contact = db.Column(db.String)
    teacher = db.Column(db.String)
    date = db.Column(db.DateTime)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    remark = db.Column(db.String)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

    @property
    def status(self):
        now = datetime.now()
        timedelta = now - self.date
        if timedelta.days > 0:
            return '已结束'
        elif timedelta.days < 0:
            return '未开始'
        elif timedelta.days == 0:
            now = current_day_seconds()
            if self.start <= now and now <= self.end:
                return '正在进行'
            if now < self.start:
                return '未开始'
            if now > self.end:
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
            'start': self.start,
            'end': self.end,
            'date': self.date.timestamp(),
            'status': self.status,
            'teacher': self.teacher,
            'contact': self.contact
        }

    @staticmethod
    def from_json(json_post):
        return Order(user_id=json_post['userID'],
                     room_id=json_post['roomID'],
                     date=datetime.fromtimestamp(json_post['date']),
                     start=json_post['start'],
                     end=json_post['end'],
                     teacher=json_post['teacher'],
                     contact=json_post['contact'],
                     )
