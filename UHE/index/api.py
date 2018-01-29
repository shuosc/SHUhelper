from flask import Blueprint, jsonify, request, current_app
from qiniu import Auth
from flask_login import login_required
from UHE.calendar.api import now
from .models import Link

index = Blueprint('index', __name__)

@index.route('/')
@login_required

def welcome():
    return jsonify('hello')

@index.route('/apps')
def get_apps():
    pass

@index.route('/upload/token')
def get_token():
    key = request.args.get('key', '')
    q = Auth(current_app.config["QINIU_ACCESS_KEY"],
             current_app.config["QINIU_SECRET_KEY"])
    return jsonify(uptoken=q.upload_token('shuhelper3'))

@index.route('/time/')
def time():
    return now()
