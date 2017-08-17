from flask import Blueprint, jsonify, current_app, request
from qiniu import Auth, put_file, put_data, BucketManager
import requests
from PIL import Image
from io import BytesIO
upload = Blueprint('upload', __name__)


@upload.route('/token')
def get_token():
    key = request.args.get('key', '')
    q = Auth(current_app.config["QINIU_ACCESS_KEY"],
             current_app.config["QINIU_SECRET_KEY"])
    return jsonify(uptoken=q.upload_token('shuhelper3'))


@upload.route('/avatar/<card_id>')
def get_avatar(card_id):
    r = requests.get(
        'http://www.tinygraphs.com/squares/{}?theme=frogideas&numcolors=4&fmt=jpg'.format(card_id))
    # i = Image.open(BytesIO(r.content))
    key = 'avatar_tinygraph_{}.jpg'.format(card_id)
    q = Auth(current_app.config["QINIU_ACCESS_KEY"],
             current_app.config["QINIU_SECRET_KEY"])
    bucket = BucketManager(q)
    token = q.upload_token('shuhelper3', key, 3600)
    ret, info = bucket.delete('shuhelper3', key)
    print(info)
    ret, info = put_data(token, key, BytesIO(r.content))
    print(info)
    return key
