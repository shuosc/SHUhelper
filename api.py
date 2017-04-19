"""
Define all api
"""

import datetime
import json
import os.path as op
import random

from flask import Flask, Response, jsonify, request, session
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.mongoengine import ModelView

import empty_room
import find_free_time
import schooltime
from adminview import *
from client import *
from config import CACHE, app
from models import *

app.config.from_pyfile('config.py')
# mail = Mail(app)
"""
admin view start 
"""

class UserView(ModelView):
    column_filters = ['card_id']
    column_searchable_list = ('card_id',)
    can_delete = False
    can_edit = False
    column_exclude_list = ['open_id', 'phone', 'create_time', 'email']

class UserDataView(ModelView):
    can_edit = False
    can_create = False
    column_exclude_list = ['data',]

class MessagesView(ModelView):
    form_ajax_refs = {
        'sender': {
            'fields': ['card_id']
        },
        'receiver':{
            'fields': ['card_id']
        }
    }
class PostView(ModelView):
    column_searchable_list = ('title',)
    form_ajax_refs = {
        'author': {
            'fields': ['card_id']
        }
    }
admin = Admin(app, name='SHUhelper', template_mode='bootstrap3')
admin.add_view(UserView(User))
admin.add_view(UserDataView(UserData))
admin.add_view(MessagesView(Messages))
admin.add_view(ModelView(Sweetie))
admin.add_view(ModelView(Functions))
admin.add_view(ModelView(MessageBoard))
admin.add_view(PostView(Post))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

"""
end adminview defines
"""

SWEEITE = Sweetie.objects(visible=True)

PUBLICATIONS = ['123']

def token():
    """
    generate random token, lenth is 8.
    """
    import random
    import string
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt

@app.route('/')
def test():
    """
    just a test
    """
    return 'hey~it\'s working'

@app.route('/publications')
def publication():
    """
    get publications from db
    """
    return random.choice(PUBLICATIONS)

@app.route('/sweetie')
def random_sweetie():
    """
    a sweet word, wish you a good day
    """
    return random.choice(SWEEITE).content

@app.route('/functions')
def get_functions():
    """
    get functions list for index page, havn't enabled now
    """
    functions = Functions.objects()
    result = []
    for function in functions:
        result.append({ 
            'tittle': function.tittle,
            'icon': function.icon,
            'url': function.url,
            'desc':function.desc
        })
    return jsonify(result)

@app.route('/accounts/login', methods=['POST'])
def login():
    """
    use services.shu.edu.cn to validate user login
    """
    post_data = json.loads(request.get_data().decode('utf-8'))
    client = Services()
    client.card_id = post_data['card_id']
    client.password = post_data['password']
    if client.login() and client.get_data():
        user = User.objects(card_id=post_data['card_id']).first()
        if user == None:
            user = User(name=client.data['name'], nickname=client.data['nickname'], card_id=post_data['card_id'],role='student')
        user.token = token()
        result = {
            'success': True,
            'token': user.token,
            'name': user.name,
            'nickname': user.nickname
        }
        session['card_id'] = user.card_id
        CACHE.set(user.token, post_data['card_id'], timeout=86400)
        user.save()
    else:
        result = {
            'success': False,
        }
    return jsonify(result)

@app.route('/accounts/logout')
def logout():
    """
    pop the cardID if in session
    """
    token = request.args.get('token')
    CACHE.delete(token)
    session.pop('card_id', None)
    return jsonify({
        'success': True
    })
@app.route('/accounts/login-with-token')
def token_login():
    """
    use token to verify user, token expired in 2 days
    """
    token = request.args.get('token')
    if CACHE.get(token) != None:
        CACHE.set(token, CACHE.get(token), timeout=86400)
        session['card_id'] = CACHE.get(token)
        result = {
            'success': True,
            }
    else:
        result = {
                'success': False,
                'status':'token_expired'
            }
    return jsonify(result)

@app.route( '/accounts/update')
def update_account():
    """
    not enabled yet
    """
    post_data = json.loads(request.get_data().decode('utf-8'))
    card_id = session['card_id']
    user = User.objects(card_id=post_data['card_id']).first()
    user.email = post_data['email']
    user.phone = post_data['phone']
    user.save()
    result = {
        'success': True
    }
    return json.dumps(result)

@app.route('/accounts/clear')
def delete_account():
    """
    considering
    """
    # later
    pass

@app.route('/messageboard',methods=['POST', 'GET'])
def messageboard():
    if request.method == 'GET':
        messages_set = MessageBoard.objects().order_by('-create_time')
        messages = []
        for message in messages_set:
            messages.append({
                'name':message.name,
                'content':message.content
            })
        return jsonify(messages)
    else:
        post_data = json.loads(request.get_data().decode('utf-8'))
        message = MessageBoard(name=post_data['name'],content=post_data['content'])
        message.save()
        return jsonify({'success':True})


@app.route('/classrooms/empty')
def findemptyroom():
    week = request.args.get('week')
    day = request.args.get('day')
    time = request.args.get('time')
    if (not week or not day or not time):
        result = {
            'week': schooltime.this_week(),
            'day': schooltime.this_day(),
            'time': schooltime.this_class(),
            'rooms': empty_room.get_emptyroom_now()
        }
    else:
        result = {
            'week': week,
            'day': day,
            'time': time,
            'rooms': empty_room.get_emptyroom(int(week), int(day), int(time))
        }
    return jsonify(result)

@app.route('/classrooms/<room>')
def room_schedule(room):
    result = {
        'room': room,
        'schedule': empty_room.get_room_schedule(room)
    }
    return jsonify(result)

# @app.route('/findemptyroom/room')
# def get_room_schedule():
#     result = {
#         'room': schooltime.this_week(),
#         'week': schooltime.this_day(),
#         'schedule': emptyroom.get_room_schedule(room, week)
#     }
#     return jsonify(result)


@app.route('/findfreetime', methods=['POST', 'GET'])
def findfreetime_member():
    if request.method == 'POST':
        usr = session['card_id']
        post_data = json.loads(request.get_data().decode('utf-8'))
        schedule = post_data['schedule']
        week = post_data['week']
        code = post_data['code']
        time_list = find_free_time.get_binary_json_from_course_table(schedule,week)
        time_lists = [] if CACHE.get(code) is None else CACHE.get(code)
        time_lists.append(time_list)
        CACHE.set(code, time_lists,timeout = 600)
        return jsonify({
                'success':True
            })
    elif request.method == 'GET':
        code = request.args.get('code')
        if CACHE.get(code) is not None:
            time_lists = CACHE.get(code)
            count = len(time_lists)
            raw_list =  find_free_time.detect_conflict(time_lists)
            Traverse_list = [([1] * 5) for i in range(0,13)]
            for j in range(0,5):
                for i in range(0,13):
                    Traverse_list[i][j]=raw_list[j][i]
            return jsonify({
                'success':True,
                'answer': Traverse_list,
                'count': count
            })
        else:
            return jsonify({
                'success':False
            })


@app.route('/messages')
def get_messages():
    """
    not enabled yet, for private messages and publication and paper airplane and so on...
    """
    card_id = session['card_id']
    user = User.objects(card_id=card_id)
    messages = Messages.objects(receiver=user)
    return json.dumps(messages)

@app.route('/queries/<site>')
def get_query(site):
    """
    get encrypted cached query result from database
    """
    if ('card_id' in session) :
        card_id = session['card_id']
    else:
        return jsonify({
            'success': False,
        })
    user = User.objects(card_id=card_id).first()
    data = UserData.objects(site=site,user=user).first()
    if data != None:
        result = {
            'success': True,
            'card_id': card_id,
            'content':data.data,
            'date':data.last_modified.timestamp()
        }
    else:
        result = {
            'success': True,
            'status':'no records',
            'card_id': card_id
        }
    return json.dumps(result)

@app.route('/queries/<site>/refresh', methods=['POST', 'GET'])
def refresh_query(site):
    """
    update query result if it doesn't exists or expried, use user ID and password and captcha (if there is)
    """
    card_id = session['card_id']
    if request.method == 'GET':
        if site == 'tiyu':
            client = Tiyu()
        elif site == 'xk':
            client = XK()
        elif site == 'cj':
            client = CJ()
        elif site == 'fin':
            client = Fin()
        elif site == 'phylab':
            client = Phylab()
        elif site == 'lehu':
            client = Lehu()
        elif site == 'services':
            client = Services() 
        CACHE.set(card_id + site, client, timeout=300)
        return jsonify({
            'success': True,
            'captcha_img':client.captcha_img
        })
    else:
        post_data = json.loads(request.get_data().decode('utf-8'))
        client = CACHE.get(card_id + site)
        client.set_account(post_data['card_id'], post_data['password'], post_data['captcha'])
        if client.login():
            if client.get_data():
                result = {
                    'success':True,
                    'content':{
                        'type': 'html',
                        'data': client.to_html()
                    }
                }
            else:
                result = {
                    'success': False,
                    'status': 'fail in get data'
                }
        else:
            result = {
                    'success': False,
                    'status': '请检查用户名密码验证码是否正确，也可能是服务器宕机'
                }
        return jsonify(result)

@app.route('/queries/<site>/save', methods=['POST', 'GET'])
def cache_query_result(site):
    """
    save encrypted query result sent from client to database 
    """
    card_id = session['card_id']
    post_data = json.loads(request.get_data().decode('utf-8'))
    user = User.objects(card_id=card_id).first()
    data = UserData.objects(site=site,user=user).first()
    if data != None:
        data.data = post_data['data']
        data.last_modified = datetime.datetime.now
    else:
        data = UserData(data=post_data['data'], site=site, user=user, last_modified=datetime.datetime.now)
    data.save()
    result = {'success':True}
    # result = {'success':False}
    return jsonify(result)

@app.route('/news/new')
def latest_news():
    """
    it will be useful
    """
    pass

@app.route('/posts')
def get_posts():
    """
    for blog system
    """
    pass

@app.route('/courses')
def get_courses():
    """
    for course query system
    """
    pass

@app.route('/services/quit')
def quit_shu():
    """
    one key to quit SHU
    """
    pass

@app.route('/services/classrooms')
def get_rooms():
    """
    a lists show all classrooms and how it's used
    """
    pass

@app.route('/services/empty-roooms')
def get_empty_rooms():
    """
    as it's name
    """
    pass


if __name__ == '__main__':
    """
    here, begins
    """
    app.debug = True
    app.run()
