import datetime

from flask import Blueprint, abort, current_app, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from mongoengine.queryset.visitor import Q

from UHE.calendar.models import Activity, Event
from UHE.client import Services
from UHE.email import send_async_email
from UHE.extensions import captcha_solver, redis_store
from UHE.upload import get_avatar
from UHE.user.models import User, UserData
from UHE.utils import make_token
import json
users = Blueprint('users', __name__)


@users.route('/data/<identifier>', methods=['GET', 'POST'])
@login_required
def user_data(identifier):
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
        client = user_data.get_client()
        if client is None:
            Client = current_app.client[identifier]
            client = Client(
                username=args.get('username'),
                password=args.get('password'),
            )
            user_data.client_id = 'client' + \
                args.get('username') + make_token()
            redis_store.set(user_data.client_id, client)
        user_data.save()
        update_user_data.delay(user_data._id)
        return jsonify(user_data)


@users.route('/replace-avatar')
@login_required
def change_avatar():
    user = User.objects.get_or_404(card_id=current_user.id)
    user.avatar = request.args.get('avatar') + '-avatar'
    user.save()
    return jsonify(status='ok')


@users.route('/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if request.method == 'GET':
        user = User.objects.get_or_404(card_id=user_id)
        return jsonify(user)
    else:
        user = User.objects.get_or_404(card_id=user_id)
        args = request.get_json()
        user.avatar = args.get('avatar', '')
        return jsonify(user)
        # user_db = {
        #     'avatar': args.get('avatar',''),
        #     'nickname': args.get()
        # }

# @users.route('/')


@users.route('/send')
def send():
    task = send_async_email.delay(subject='hello', recipients=[
                                  current_app.config["TESTING_EMAIL"]], text_body='hello', html_body='hllo')
    return task.id


@users.route('/test')
def test():
    return current_app.test


@users.route('/search/<query>')
def search(query):
    users = User.objects(Q(card_id__contains=query) |
                         Q(name__contains=query))[:50]
    return jsonify([{
        '_id': user.card_id,
        'name': user.name[0] + '*' * len(user.name[1:])
    }for user in users])


@users.route('/xk')
def xk():
    # print(client.captcha_img)
    # captcha = result(client.captcha_img)
    answer = captcha_solver.create(client.captcha_img)
    return answer['Result']


@users.route('/delete')
def delete():
    event = Event.objects(identifier="SHU_base_schedule").first()
    print(event)
    print(Activity.objects(event=event))
    Activity.objects(event=event).delete()
    return 'success'


@users.route('/reset-avatar')
@login_required
def reset_avatar():
    user = User.objects(id=current_user.id).first()
    user.avatar = get_avatar(user.card_id)
    user.save()
    return jsonify(status='ok')


@users.route('/init-avatar/<card_id>')
def init_avatar(card_id):
    user = User.objects(card_id=card_id).first()
    user.avatar = get_avatar(user.card_id)
    user.save()
    return jsonify(status='ok')


@users.route('/logout')
def logout():
    token = request.args.get('token')
    if token is not None:
        redis_store.delete(token)
    logout_user()
    return jsonify({
        'success': True
    })


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
