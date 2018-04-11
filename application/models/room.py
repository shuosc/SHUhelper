"""
api.py
"""
from flask import Flask, request, jsonify
from application.extensions import db
from flask.views import MethodView
from application.models.user import User
from application.enums import Campus
from datetime import datetime
import requests
from sqlalchemy.dialects.postgresql import ENUM

class Room(db.Model):
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


class Order(db.Model):
    __tablename__ = 'room_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    date = db.Column(db.DateTime)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    remark = db.Column(db.String)
    # room = db.relationship('Room',backref=db.backref('orders', lazy=True))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id':self.id,
            'userID': self.user_id,
            'roomID': self.room_id,
            'room': self.room.name,
            'start': self.start,
            'end': self.end,
            'date': self.date.timestamp()
        }

    @staticmethod
    def from_json(json_post):
        return Order(user_id=json_post['userID'],
                     room_id=json_post['roomID'],
                     date=datetime.fromtimestamp(json_post['date']),
                     start=json_post['start'],
                     end=json_post['end'])
