import datetime

from flask import Blueprint, request, jsonify, current_app, abort, redirect, url_for, flash
from flask_login import login_user, logout_user

from UHE.client import Services
from UHE.email import send_async_email
from UHE.extensions import captcha_solver, redis_store
from UHE.user.models import User
from UHE.utils import make_token,validate
from UHE.plugins.SHU_course import get_term
index = Blueprint('index', __name__)


@index.route('/<card_id>')
def profile(card_id):
    user = User.objects.get_or_404(card_id=card_id)
    return jsonify(user.json)


@index.route('/send')
def send():
    task = send_async_email.delay(subject='hello', recipients=[
                                  current_app.config["TESTING_EMAIL"]], text_body='hello', html_body='hllo')
    return task.id


@index.route('/term')
def test_get_term():
    term = get_term('http://xk.shu.edu.cn:8080')
    return term


@index.route('/term/async')
def test_get_term_async():
    term = get_term.delay('http://xk.shu.edu.cn:8080')
    return term.get()





@index.route('/test')
def test():
    return current_app.test


@index.route('/xk')
def xk():
    # print(client.captcha_img)
    # captcha = result(client.captcha_img)
    answer = captcha_solver.create(client.captcha_img)
    return answer['Result']


@index.route("/login/", methods=['POST'])
def login():
    """
    use services.shu.edu.cn to validate user login
    """
    post_data = request.get_json()
    client = Services(post_data['card_id'], post_data['password'])
    if client.login() and client.get_data():
        user = User.objects(card_id=post_data['card_id']).first()
        if user is None or not user.activated:
            user = User(name=client.data['name'], nickname=client.data['nickname'],
                        card_id=post_data['card_id'], role='student', activated=True)
        user.token = make_token()
        result = {
            'token': user.token,
            'name': user.name,
            'nickname': user.nickname
        }
        redis_store.set('token_' + user.token, post_data['card_id'], ex=86400)
        user.last_login = datetime.datetime.now()
        user.save()
        login_user(user)
    else:
        abort(401)
    return jsonify(result)


@index.route("/login-with-token/")
def login_with_token():
    token = request.args.get('token')
    card_id = redis_store.get('token_' + token, '0')
    user = User.objects(card_id=card_id).first()
    if user:
        result = {
            'token': user.token,
            'name': user.name,
            'nickname': user.nickname
        }
        redis_store.set('token_' + user.token, card_id, ex=86400)
        user.last_login = datetime.datetime.now()
        user.save()
        login_user(user)
    else:
        abort(401)
    return jsonify(result)
