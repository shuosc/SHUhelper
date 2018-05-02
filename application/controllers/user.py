import datetime
import json

from flask import Blueprint, abort, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from application.services.sim_clients import *
from application.extensions import redis_store
from application.models.user import User, UserData

users = Blueprint('users', __name__)

CLIENTS = {
    'physical-exercise': Tiyu,
    'basic-info': Services,
    'my-course': XK,
    'grade': CJ
}


def refresh_data(name, card_id, password, lock):
    user_data = UserData.query.filter_by(
        user=card_id, name=name).first()
    user_data.status = 'pending'
    user_data.save()
    client_class = CLIENTS[name]
    try:
        client = client_class(card_id, password)
        client.login()
        client.get_data()
    except Exception as e:
        user_data.status = 'failed'
        user_data.last_modified = datetime.datetime.now()
        user_data.save()
        print('error')
        raise e
    user_data.data = client.to_json()
    user_data.status = 'success'
    user_data.last_modified = datetime.datetime.now()
    user_data.lock_save(lock)
    return True


@users.route('/data/<name>', methods=['GET', 'POST'])
@login_required
def user_data(name):
    if request.method == 'GET':
        user_data = UserData.query.filter_by(
            user=current_user.id, name=name).first_or_404()
        return jsonify(user_data.to_json())
    else:
        post_data = request.get_json()
        user_data = UserData.query.filter_by(
            user=current_user.id, name=name).first()
        if user_data is None:
            user_data = UserData(name=name,
                                 user=current_user.id, status='none')
            user_data.save()
        password = post_data.get('pw') # delete these in next release
        if password is None:
            password = post_data.get('password')
        task = refresh_data(name, current_user.id,
                            password, password)
        return jsonify(success='ok')


# @users.route('/replace-avatar')
# @login_required
# def change_avatar():
#     user = User.objects.get_or_404(card_id=current_user.id)
#     user.avatar = request.args.get('avatar') + '-avatar'
#     user.save()
#     return jsonify(status='ok')


# @users.route('/search/<query>')
# def search(query):
#     users = User.objects(Q(card_id__contains=query) |
#                          Q(name__contains=query))[:50]
#     return jsonify([{
#         '_id': user.card_id,
#         'name': user.name[0] + '*' * len(user.name[1:])
#     }for user in users])

# @users.route('/<user_id>')
# def profile(user_id):
#     user = User.objects.get_or_404(card_id=user_id)
#     return jsonify(avatar=user.avatar, nickname=user.nickname, _id=user.id)


# @users.route('/<user_id>/custom', methods=['GET', 'PATCH'])
# @login_required
# def user_custom(user_id):
#     if user_id != current_user.id:
#         abort(401)
#     if request.method == 'GET':
#         user = User.objects.get_or_404(card_id=current_user.id)
#         return jsonify(user.custom)
#     else:
#         user = User.objects(card_id=current_user.id).first()
#         custom = json.loads(user.custom) if user.custom != '' else {}
#         patch = request.get_json()
#         for key in patch.keys():
#             custom[key] = patch[key]
#         user.custom = json.dumps(custom)
#         user.save()
#     return jsonify(avatar=user.avatar, nickname=user.nickname, _id=user.id)


# @users.route('/set-custom-theme')
# def set_custom_theme():
#     theme = request.args.get('theme')
#     user = User.objects(card_id=current_user.id).first()
#     custom = json.loads(user.custom) if user.custom != '' else {}
#     custom['theme'] = theme
#     user.custom = json.dumps(custom)
#     user.save()
#     return jsonify({
#         'status': 'ok'
#     })
