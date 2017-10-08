import datetime

from flask import Blueprint, abort, current_app, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from mongoengine.queryset.visitor import Q

from UHE.calendar.models import Activity, Event
from UHE.client import Services, Fin, Tiyu, SZ
from UHE.email import send_async_email
from UHE.extensions import captcha_solver, redis_store
from UHE.upload import get_avatar
from UHE.user.models import User, UserData
from UHE.utils import make_token
import json
users = Blueprint('users', __name__)


@users.route('/<card_id>/data/<identifier>/', methods=['GET', 'POST'])
@login_required
def user_data(card_id, identifier):
    identifier = 'tiyu'
    if request.method == 'GET':
        user_data = UserData.objects.get_or_404(
            user=current_user.id, identifier=identifier)
        return jsonify(user_data)
    else:
        args = request.get_json()
        user_data = UserData.objects(
            user=current_user.id, identifier=identifier).first()
        if user_data is None:
            user_data = UserData(user=current_user.id, identifier=identifier)
            user_data.save()
        post_data = request.get_json()
        user_data = UserData.objects(
            user=current_user.id, identifier=identifier).first()
        if user_data is None:
            user_data = UserData(identifier=identifier,
                                 user=current_user.id, status='none')
            user_data.save()
        task = get_data(identifier, current_user.id,
                        post_data['password'], post_data['password'])
        return jsonify(success='ok')


def get_data(identifier, card_id, password, lock):
    user_data = UserData.objects(user=card_id, identifier=identifier).first()
    user_data.status = 'pending'
    user_data.save()
    try:
        client = Tiyu(card_id, password)
        client.login()
        client.get_data()
    except Exception as e:
        user_data.status = 'failed'
        user_data.save()
        print('error')
        raise e
    user_data.data = client.to_json()
    user_data.status = 'success'
    user_data.last_modified = datetime.datetime.now()
    user_data.lock_save(lock)


@users.route('/replace-avatar')
@login_required
def change_avatar():
    user = User.objects.get_or_404(card_id=current_user.id)
    user.avatar = request.args.get('avatar') + '-avatar'
    user.save()
    return jsonify(status='ok')


@users.route('/search/<query>')
def search(query):
    users = User.objects(Q(card_id__contains=query) |
                         Q(name__contains=query))[:50]
    return jsonify([{
        '_id': user.card_id,
        'name': user.name[0] + '*' * len(user.name[1:])
    }for user in users])


@users.route('/logout')
def logout():
    token = request.args.get('token')
    if token is not None:
        redis_store.delete(token)
    logout_user()
    return jsonify({
        'success': True
    })


@users.route('/<user_id>')
def profile(user_id):
    user = User.objects.get_or_404(card_id=user_id)
    return jsonify(avatar=user.avatar, nickname=user.nickname, _id=user.id)


@users.route('/<user_id>/custom', methods=['GET', 'PATCH'])
@login_required
def user_custom(user_id):
    if user_id != current_user.id:
        abort(401)
    if request.method == 'GET':
        user = User.objects.get_or_404(card_id=current_user.id)
        return jsonify(user.custom)
    else:
        user = User.objects(card_id=current_user.id).first()
        custom = json.loads(user.custom) if user.custom != '' else {}
        patch = request.get_json()
        for key in patch.keys():
            custom[key] = patch[key]
        user.custom = json.dumps(custom)
        user.save()
    return jsonify(avatar=user.avatar, nickname=user.nickname, _id=user.id)


@users.route('/set-custom-theme')
def set_custom_theme():
    theme = request.args.get('theme')
    user = User.objects(card_id=current_user.id).first()
    custom = json.loads(user.custom) if user.custom != '' else {}
    custom['theme'] = theme
    user.custom = json.dumps(custom)
    user.save()
    return jsonify({
        'status': 'ok'
    })


@users.route("/login/", methods=['POST'])
def login():
    """
    use services.shu.edu.cn to validate user login
    """
    post_data = request.get_json()
    success = False
    try:
        client = Services(post_data['card_id'], post_data['password'])
        success = client.login() and client.get_data()
    except:
        client = SZ(post_data['card_id'], post_data['password'])
        success = client.login() and client.get_data()
    if success:
        user = User.objects(card_id=post_data['card_id']).first()
        if user is None:
            user = User(name=client.data['name'], nickname=client.data.get('nickname'),
                        card_id=post_data['card_id'], role='student', activated=True)
        elif not user.activated:
            user.name = client.data['name']
            user.nickname = client.data.get('nickname')
            user.activated = True
        nickname = client.data.get('nickname')
        if nickname is not None and user.nickname != nickname:
            user.nickname = nickname
        user.token = make_token()
        result = {
            'avatar': user.avatar,
            'token': user.token,
            'name': user.name,
            'nickname': user.nickname,
            'custom': user.custom
        }
        redis_store.set('token_' + user.token, post_data['card_id'], ex=86400)
        user.last_login = datetime.datetime.now()
        user.save()
        login_user(user)
        return jsonify(result)
    else:
        abort(401)


@users.route("/login-with-token/")
def login_with_token():
    token = request.args.get('token')
    card_id = redis_store.get('token_' + token)
    user = User.objects(card_id=card_id).first()
    if user:
        user.token = token
        result = {
            'avatar': user.avatar,
            'token': user.token,
            'name': user.name,
            'nickname': user.nickname,
            'custom': user.custom
        }
        redis_store.set('token_' + user.token, user.card_id, ex=86400)
        user.last_login = datetime.datetime.now()
        user.save()
        login_user(user)
        return jsonify(result)
    else:
        abort(401)
