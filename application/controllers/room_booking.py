from datetime import datetime
from functools import reduce

import requests
from flask import Blueprint, Flask, jsonify, request, current_app
from flask.views import MethodView
from flask_login import current_user, login_required

from application.extensions import db
from application.models.room import Order, Room
from application.utils import current_ten_minutes, current_day_seconds
from sqlalchemy import cast,Integer
rooms = Blueprint('room', __name__)
room_orders = Blueprint('room_order', __name__)


def render_room_info(room, orders):
    return {
        'id': room.id,
        'name': room.name,
        # 'schedule': schedule,
        'orders': [order.to_json() for order in orders]
    }


def render_rooms_info(rooms, orders):
    return [render_room_info(room, filter(lambda x:str(x.room_id) == str(room.id), orders)) for room in rooms]


def cal_restrict(orders):
    used = reduce(lambda x, y: x + (y.end-y.start+1), orders, 0)
    return 4*3600 - used


def check_restrict(order, user_id):
    orders = Order.query.filter_by(date=order.date, user_id=user_id).all()
    restrict = cal_restrict(orders)
    return restrict >= (order.end-order.start + 1)


@rooms.route('', methods=['GET'])
@login_required
def get_rooms():
    now = datetime.now()
    timestamp = request.args.get('timestamp', datetime(
        now.year, now.month, now.day).timestamp(), int)
    group = request.args.get('group', 'ces')
    rooms = Room.query.order_by(cast(Room.name, Integer)).filter_by(
        available=True, group=group).all()
    orders = Order.query.filter_by(
        date=datetime.fromtimestamp(timestamp)).all()
    user_orders = filter(lambda x: x.user_id == current_user.id, orders)
    restrict = cal_restrict(user_orders)
    return jsonify(rooms=render_rooms_info(rooms, orders), restrict=restrict)


@rooms.route('/<room_id>', methods=['GET'])
@login_required
def get_room(room_id):
    now = datetime.now()
    room = Room.query.get(room_id)
    timestamp = request.args.get('timestamp', datetime(
        now.year, now.month, now.day).timestamp(), int)
    orders = Order.query.filter_by(
        room_id=room_id, date=datetime.fromtimestamp(timestamp)).all()
    user_orders = filter(lambda x: x.user_id == current_user.id, orders)
    restrict = cal_restrict(user_orders)
    return jsonify(room=render_room_info(room, orders), restrict=restrict)


def check_room_available(order):
    orders = Order.query.filter_by(
        room_id=order.room_id, date=order.date).all()
    for valid_order in orders:
        if valid_order.end < order.start or order.end < valid_order.start:
            continue
        else:
            return False
    return True


class OrderAPI(MethodView):
    decorators = [login_required]

    def get(self, order_id):
        if order_id is None:
            orders_type = request.args.get('type', 'personal')
            if orders_type == 'personal':
                orders = Order.query.filter_by(
                    user_id=current_user.id).order_by(Order.date.desc()).all()
                return jsonify(orders=[order.to_json() for order in orders])
        else:
            order = Order.query.filter_by(id=order_id).first()
            return jsonify(order=order.to_json())

    def post(self):
        now = datetime.now()
        nowaday = datetime(now.year, now.month, now.day)
        json = request.json
        json['userID'] = current_user.id
        order = Order.from_json(json)

        if check_restrict(order, current_user.id) == False:
            return jsonify(msg='您当日借教室时长配额不足'), 400
        if check_room_available(order) == False:
            return jsonify(msg='该时间段已被占用'), 400
        timedelta = order.date - nowaday
        if timedelta.days < 0 or timedelta.days > 3:
            return jsonify(msg='该日无法预约'), 400
        if timedelta.days == 0 and current_day_seconds() > order.start:
            return jsonify(msg='您选择的时段已过，无法预约'), 400
        order.save()
        return jsonify(order=order.to_json())

    def delete(self, order_id):
        if order_id is None:
            return jsonify(msg="无权限"), 401
        else:
            order = Order.query.filter_by(id=order_id).first()
            if not order.user_id == current_user.id:
                return jsonify(msg="无权限"), 401
            order.delete()
            return jsonify(sucroom_orders=True)

    def put(self, order_id):
        order = Order.query.filter_by(id=order_id).first()
        if not order.user_id == current_user.id:
            return jsonify(msg="无权限"), 401
        seconds = current_day_seconds()
        end = seconds - seconds%(600) + 600
        if end >= order.start and end <= order.end:
            order.end = end
            order.save()
        return jsonify(order=order.to_json())


room_view = OrderAPI.as_view('order_api')
room_orders.add_url_rule('/', defaults={'order_id': None},
                         view_func=room_view, methods=['GET', ])
room_orders.add_url_rule('/', view_func=room_view, methods=['POST', ])
room_orders.add_url_rule('/<order_id>', view_func=room_view,
                         methods=['GET', 'PUT', 'DELETE'])
