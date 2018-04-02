"""
api.py
"""
from flask import Flask,request,jsonify
from UHE.extensions import db
from flask.views import MethodView
from UHE.user.models import User
from datetime import datetime
import requests

class Room(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    detail = db.Column(db.String(80), nullable=False)
    available = db.Column(db.Boolean,default=True)
    # orders = db.relationship('User', secondary=orders, lazy='subquery',
    #     backref=db.backref('rooms', lazy=True))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    create_time = db.Column(db.DateTime)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    remark = db.Column(db.String)
    room = db.relationship('Room',backref=db.backref('orders', lazy=True))
    def to_json(self):
        return {
            'userID':self.user_id,
            'roomID':self.room_id,
            'start':self.start,
            'end':self.end
        }
    @staticmethod 
    def from_json(json_post):
        return Order(**json_post)
