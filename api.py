"""
Define all api
"""
import os.path as op
from flask import Flask, session, Response, jsonify, request
from client import *
import random
from werkzeug.contrib.cache import MemcachedCache
from werkzeug.contrib.cache import SimpleCache
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from models import *
from flask_mongoengine import MongoEngine
from flask_admin.contrib.mongoengine import ModelView
import json

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'psyduckdev'}
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = MongoEngine()
db.init_app(app)
class UserView(ModelView):
    column_filters = ['card_id']
    column_searchable_list = ('card_id',)

class MessagesView(ModelView):
    form_ajax_refs = {
        'sender': {
            'fields': ['card_id']
        },
        'receiver':{
            'fields': ['card_id']
        }
    }

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(UserView(User))
admin.add_view(ModelView(UserData))
admin.add_view(MessagesView(Messages))
admin.add_view(ModelView(Sweetie))
admin.add_view(ModelView(Functions))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
# admin.add_view(FileAdmin('/', '/source/', name='source code'))

SWEEITE = Sweetie.objects(visible=True)
CACHE = SimpleCache()
PUBLICATIONS = ['123']

def token():
    """
    generate random token, lenth is 8.
    """
    import random
    import string
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt

class User_Login():
    def __init__(self):
        self.clent = None
        self.card_id = ''
        self.session = ''
        self.token = ''

@app.route('/')
def test():
    return 'hey~it\'s working'

@app.route('/publications')
def publication():
    return random.choice(PUBLICATIONS)

@app.route('/sweetie')
def random_sweetie():
    return random.choice(SWEEITE).content

@app.route('/functions')
def get_functions():
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
    post_data = json.loads(request.get_data().decode('utf-8'))
    client = Services()
    client.card_id = post_data['card_id']
    client.password = post_data['password']
    client.login()
    if client.is_login:
        client.get_data()
        user = User.objects(card_id=post_data['card_id'])
        if user is None:
            user = User(name=client.name, username=client.username, card_id=post_data['card_id'],role='student')
        user.token = token()
        result = {
            'success': True,
            'token': user.token,
            'name': user.name,
            'username': user.username
        }
        session['card_id'] = user.card_id
        CACHE.set(user.token, post_data['card_id'], timeout=0)
        user.save()
    else:
        result = {
            'success': False,
        }
    return json.dumps(result)

@app.route('/accounts/login-with-token')
def token_login():
    token = request.args.get('token')
    session['card_id'] = CACHE.get(token)
    if session['card_id'] != None:
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
    post_data = json.loads(request.get_data().decode('utf-8'))
    card_id = session['card_id']
    user = User.objects(card_id=post_data['card_id'])
    user.email = post_data['email']
    user.phone = post_data['phone']
    user.save()
    result = {
        'success': True
    }
    return json.dumps(result)

@app.route('/accounts/clear')
def delete_account():
    # later
    pass

@app.route('/messages')
def get_messages():
    card_id = session['card_id']
    user = User.objects(card_id=card_id)
    messages = Messages.objects(receiver=user)
    return json.dumps(messages)

@app.route('/queries/<site>')
def get_query(site, subject):
    card_id = session['card_id']
    user = User.objects(card_id=card_id)
    data = UserData.objects(site=site,user=user)
    if data != None:
        result = {
            'success': True,
            'content':data.content,
            'date':data.last_modified
        }
    else:
        result = {
            'success': True,
            'status':'no records'
        }
    return json.dumps(result)

@app.route('/queries/<site>/refresh', methods=['POST', 'GET'])
def refresh_query(site):
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
        elif site == 'Phylab':
            client = Phylab()
        elif site == 'lehu':
            client = Lehu()
        elif site == 'services':
            client = Services()
        CACHE.set(card_id + site, client, timeout=300)
        return json.dumps({
            'status':'success',
            'sesion': session[site],
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
                    'content':client.to_json()
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
def cache_query_result():
    card_id = session['card_id']
    try:
        post_data = json.loads(request.get_data().decode('utf-8'))
        user = User.objects(card_id=card_id)
        data = UserData(data=post_data['data'], site=site, user=user, last_modified=datetime.datetime.now)
        data.save()
        result = {'success':True}
    except:
        result = {'success':False}
    return jsonify(result)

@app.route('/news/new')
def latest_news():
    pass

@app.route('/posts')
def get_posts():
    pass

@app.route('/courses')
def get_courses():
    pass

@app.route('/services/find-free-time')
def find_free_time():
    pass

@app.route('/services/quit')
def quit_shu():
    pass

@app.route('/services/classrooms')
def get_rooms():
    pass

@app.route('/services/empty-roooms')
def get_empty_rooms():
    pass


if __name__ == '__main__':
    app.debug = True
    app.run()