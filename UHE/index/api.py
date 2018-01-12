from flask import Blueprint, jsonify, request, abort,current_app,redirect
from flask.views import MethodView
from flask_login import current_user
from qiniu import Auth, put_data, BucketManager
from .models import Link
from UHE.calendar.api import now
index = Blueprint('index', __name__)

index.route('/')
def welcome():
    return jsonify('hello')

@index.route('/link/<identifier>')
def get_link(identifier):
    link = Link.objects.get_or_404(identifier=identifier)
    return jsonify(link)

@index.route('/upload/token')
def get_token():
    key = request.args.get('key', '')
    q = Auth(current_app.config["QINIU_ACCESS_KEY"],
             current_app.config["QINIU_SECRET_KEY"])
    return jsonify(uptoken=q.upload_token('shuhelper3'))

@index.route('/time/')
def time():
    return now()

# @index.route('/avatar/<card_id>')
# def get_avatar(card_id):
#     r = requests.get(
#         'http://www.tinygraphs.com/squares/{}?theme=frogideas&numcolors=4&fmt=jpg'.format(card_id))
#     # i = Image.open(BytesIO(r.content))
#     key = 'avatar_tinygraph_{}_{}.jpg'.format(card_id, make_token())
#     q = Auth(current_app.config["QINIU_ACCESS_KEY"],
#              current_app.config["QINIU_SECRET_KEY"])
#     bucket = BucketManager(q)
#     token = q.upload_token('shuhelper3', key, 3600)
#     # ret, info = bucket.delete('shuhelper3', key)
#     ret, info = put_data(token, key, BytesIO(r.content))
#     print(info)
#     return key