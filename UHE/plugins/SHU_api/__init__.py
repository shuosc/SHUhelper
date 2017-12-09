from flask import Blueprint, jsonify, request, abort
from flask.views import MethodView
from flask_login import current_user
from .client import Services
SHUapi = Blueprint('shu', __name__)

def auth_user(username,password):
    pass
    # success = False
    # user = User.objects(card_id=username).first()
    # client = Services(username,password)
    # if user is None:
    #     if client.login() and client.get_data():
    #         user = User(name=client.data['name'], nickname=client.data.get('nickname'),
    #                     card_id=post_data['card_id'], role='student', activated=True, hash=generate_password_hash(post_data['password']))
    #     else:
    #         abort(403)
    # else:
    #     if user.name != '未激活':
    #         if user.hash != '':
    #             if check_password_hash(user.hash, post_data['password']):
    #                 pass
    #             else:
    #                 if client.login():
    #                     user.hash=generate_password_hash(post_data['password'])
    #                     user.save()
    #                 else:
    #                     abort(403)
    #         else:
    #             if client.login():
    #                 user.hash=generate_password_hash(post_data['password'])
    #                 user.save()
    #             else:
    #                 abort(403)
    #     else:
    #         if  client.login() and client.get_data():
    #             user.name = client.data['name']
    #             user.nickname = client.data.get('nickname')
    #             user.hash=generate_password_hash(post_data['password'])
    #             user.save()
    #         else:
    #             abort(403)
    # user.token=make_token()
    # result={
    #     'avatar': user.avatar,
    #     'token': user.token,
    #     'name': user.name,
    #     'nickname': user.nickname,
    #     'custom': user.custom
    # }
    # redis_store.set('token_' + user.token, post_data['card_id'], ex=86400)
    # user.last_login=datetime.datetime.now()
    # user.save()
    # login_user(user)

@SHUapi.route('/news/')
def get_news_api():
    pass

@SHUapi.route('/courses/')
def get_courses_api():

    pass
    return 'ok'

@SHUapi.route('/auth/')
def auth_user_api():
    pass

