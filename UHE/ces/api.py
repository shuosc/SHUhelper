from flask import Flask,request,jsonify,Blueprint
from flask.views import MethodView
from datetime import datetime
from flask_login import login_required,current_user
from UHE.extensions import db
import requests
from .models import User,Room,Order
ces = Blueprint('ces', __name__)
# @app.route('/oauth/wx')
# def get_open_id():
#     s = requests.Session()
#     code = request.args.get('code')
#     r = s.get('https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxf6081fd49106fe2b&secret=5e6fa96a0d1a148b08e89eab098e03ef&code=%s&grant_type=authorization_code' % (code))
#     auth_result = json.loads(r.text)
#     if 'openid' in auth_result:
#         open_id = auth_result['openid']
#     return jsonify(msg='error'),401
def render_room_info(room,orders):
    schedule = [1 for i in range(13)]
    for order in orders:
        for i in range(order.start-1,order.end):
            schedule[i] = 0
    return {
        'id':room.id,
        'name': room.name,
        'schedule': schedule
    }

def render_rooms_info(rooms,orders):
    return [render_room_info(room,filter(lambda x:x.room_id==room.id,orders)) for room in rooms]

@ces.route('/rooms',methods=['GET'])
def get_rooms():
    now = datetime.now()
    timestamp = request.args.get('timestamp',datetime(now.year,now.month,now.day).timestamp(),int)
    rooms = Room.query.filter_by(available=True).all()
    orders = Order.query.filter_by(date=datetime.fromtimestamp(timestamp)).all()
    return jsonify(rooms=render_rooms_info(rooms,orders))

def get_orders_by_date(year,month,day):
    return Order.query.filter_by(year=year,month=month,day=day).all()

def check_room_available(order):
    orders = Order.query.filter_by(room_id=order.room_id,date=order.date).all()
    for valid_order in orders:
        if valid_order.end < order.start or order.end < valid_order.start:
            continue
        else:
            return False
    return True

class OrderAPI(MethodView):
    # decorators = [login_required]
    def get(self, order_id):
        if order_id is None:
            now = datetime.now()
            year = request.args.get('year',now.year,type=int)
            month = request.args.get('month',now.month,type=int)
            day = request.args.get('day',now.day,type=int)
            orders = get_orders_by_date(year,month,day)
            return jsonify(orders = [order.to_json() for order in orders],count=orders.count())
        else:
            order = Order.query.filter_by(id=order_id).first()
            return jsonify(order = order.to_json())

    def post(self):
        json = request.json
        json['userID'] = '15121604'
        order = Order.from_json(json)
        if check_room_available(order):
            order.save()
            return jsonify(order = order.to_json())
        else:
            return jsonify(msg='已被占用'),400

    def delete(self, order_id):
        order = Order.query.filter_by(id=order_id).first()
        db.session.delete(order)
        db.session.commit()
        return jsonify(success=True)

    def put(self, order_id):
        # update a single user
        pass

user_view = OrderAPI.as_view('order_api')
ces.add_url_rule('/orders/', defaults={'order_id': None},
                 view_func=user_view, methods=['GET',])
ces.add_url_rule('/orders/', view_func=user_view, methods=['POST',])
ces.add_url_rule('/orders/<int:order_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])

