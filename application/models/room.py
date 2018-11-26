from flask import Flask, request, jsonify, current_app
from application.extensions import db
from flask.views import MethodView
from application.models.user import User
from application.enums import Campus
from datetime import datetime
import requests
from sqlalchemy.dialects.postgresql import ENUM
from application.utils import CRUDMixin, current_ten_minutes, current_day_seconds, TimeMixin
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


members = db.Table('meeting_members',
                   db.Column('order_id', db.UUID(as_uuid=True), db.ForeignKey(
                       'room_booking_order.id'), primary_key=True),
                   db.Column('member_id', db.String, db.ForeignKey(
                       'user.id'), primary_key=True)
                   )


class Order(db.Model, CRUDMixin, TimeMixin):
    __tablename__ = 'room_booking_order'
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    room_id = db.Column(db.UUID, db.ForeignKey('room.id'))
    contact = db.Column(db.String)
    teacher = db.Column(db.String)
    date = db.Column(db.DateTime)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    remark = db.Column(db.String)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    members = db.relationship('User', secondary=members, lazy='subquery',
                              backref=db.backref('room_booking_orders', lazy=True))

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
                return '已开始'
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
            # 'teacher': self.teacher,
            'contact': self.contact,
            'remark': self.remark,
            'members': [member.id for member in self.members]
        }

    @staticmethod
    def from_json(json_post):
        order = Order(user_id=json_post['userID'],
                      room_id=json_post['roomID'],
                      date=datetime.fromtimestamp(json_post['date']),
                      start=json_post['start'],
                      end=json_post['end'],
                    #   teacher=json_post['teacher'],
                      contact=json_post['contact'],
                      remark=json_post['remark']
                      )
        # order.save()
        return order


# class MeetingMember(db.Model):
#     id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
#     order_id = db.Column(db.UUID, db.ForeignKey('room_booking_order.id'))
#     member_id = db.Column(db.String,db.ForeignKey('user.id'))
