
"""
api.py
"""
from flask import Flask,request,jsonify

from flask.views import MethodView
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



@app.route('/auth', methods=['POST'])
def auth():
    """
    对接SHUhelper的验证接口
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=username)}
    return jsonify(ret), 200

@app.route('/oauth/wx')
def get_open_id():
    s = requests.Session()
    code = request.args.get('code')
    r = s.get('https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxf6081fd49106fe2b&secret=5e6fa96a0d1a148b08e89eab098e03ef&code=%s&grant_type=authorization_code' % (code))
    auth_result = json.loads(r.text)
    if 'openid' in auth_result:
        open_id = auth_result['openid']
    return jsonify(msg='error'),401
def render_room_info(room):
    return {
        'id':room.id,
        'name': room.name
    }

def render_rooms_info(rooms):
    return [render_room_info(room) for room in rooms]
    pass

@app.route('/rooms',methods=['GET'])
def get_rooms():
    rooms = Room.query.filter_by(available=True).all()
    return jsonify(rooms=render_rooms_info(rooms))

def get_orders_by_date(year,month,day):
    return Order.query.filter_by(year=year,month=month,day=day).all()

def check_room_available(order):
    orders = Order.query.filter_by(\
            room_id=order.room_id,year=order.year,\
            month=order.month,day=order.day).first()
    usage = [True for i in range(13)]
    for valid_order in orders:
        if valid_order.end < order.start or order.end < valid_order.start:
            continue
        else:
            return False
    return True

class OrderAPI(MethodView):
    # decorators = [jwt_required]
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
        json['user_id'] = 1
        order = Order.from_json(json)
        if check_room_available(order):
            db.session.add(order)
            db.session.commit()
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
app.add_url_rule('/orders/', defaults={'order_id': None},
                 view_func=user_view, methods=['GET',])
app.add_url_rule('/orders/', view_func=user_view, methods=['POST',])
app.add_url_rule('/orders/<int:order_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)
