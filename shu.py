#! python3
#coding=utf-8
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response,send_from_directory
from werkzeug.contrib.cache import SimpleCache
from sqlite3 import dbapi2 as sqlite3
import sys
import string
import requests
import os
import base64
from sites import *
app = Flask(__name__)

# configuration
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'course.db'),
    DEBUG=False,
    SECRET_KEY='shuhelper',
    USERNAME='admin',
    PASSWORD='default'
))
cache = SimpleCache()
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
dailywords = [u"不是世界变得无聊，而是你变成了无聊的人",
u"DON'T PANIC",
u"总而言之，不论发生了什么，只要还没死，人生就还没有结束－－人生仍会继续。也不会出现什么片尾曲或者STAFF字幕之类的东西",
u"我们信守这些不言自明的真理：人人生而平等",
u"人们不都是喜欢看着大家的笑容活下去吗？",
u"在虚构的故事中寻找真实感的人一定脑袋有问题",
u"猫经常揣手是因为他们知道这样很萌吗？",
u"今天也肯定有某人，在世界的某个地方死去哦？所以穿丧服吧",
u"诸葛亮知识广博，乃至在三国杀中需要三张将牌才能勉强概括他的技能。",
u"英文咒语翻译成中文还有法术效果吗",
u"莱特兄弟发明飞机以前，任何人如果想要飞到其他地方，都必须将 200 磅重的氦气吃下肚。",
u"如果生活给了你土豆，就把他炸成土豆片 \(^o^)/ ",
u"你今天真好看(*^_^*)",
u"我们的成功是不应该通过企求别人的懈怠来达到的",
u"本想给你做菜，可惜我没有锅。本想给你织围巾，可惜我没有线。本想给你写首诗，可惜我没有笔。",
u"人生 ！ (/▽＼=)",
u"自强不息",
u"我们都是孤单的动物。我们把全部人生用来减轻孤独。",
u"『这个世界上不存在才华，也不存在天赋，都是把事情一遍一遍重复做，下笨功夫，的来的成绩。』",
u"『我岁数大了，就是想为国家多做贡献，其他无所挂念。』——钱伟长",
u"每逢你想要批评任何人时，请记住，这个世界上所有的人，并不是个个都有过你所拥有的那些优越条件",
u"以回赠她曾经送给我的那些可爱笑容",
u"You will make a great discovery.",
u"『这个世界上不存在才华，也不存在天赋，都是把事情一遍一遍重复做，下笨功夫，的来的成绩。』",
u"前路未必顺利，但前路一定精彩",
u"这颗星球上有无数微不足道的生命，但每一个生命都是可以歌唱的。",
u"『这个世界上不存在才华，也不存在天赋，都是把事情一遍一遍重复做，下笨功夫，的来的成绩。』",
u"年轻人是时常错过老人的",
u"所有的爱都是为了相聚，只有父母与儿女的爱是为了别离",
u"社会就是靠这种『异类』进步的呀",
u"艺术，为了艺术的艺术，是这个世界上唯一重要的事情；艺术家凭一己之力赋予这荒谬的世界以意义。"]
def randsession():
    import random
    import string
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt

def randwords():
    import random
    import string

    return random.choice(dailywords)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select user_id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None

def course_query(cid,cname,tname,tid):
    db = get_db()
    cur = db.execute('select * from courses where courseuid like "%%%s%%" and coursename like "%%%s%%" and teachname like "%%%s%%" and teachid like "%%%s%%" limit 0,200' % (cid,cname,tname,tid))
    courses = cur.fetchall()
    return courses

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/querycourse', methods=['POST', 'GET'])
def querycourse():
    flash(u'<a class="white-text" href="http://shuhelper.cn/article/2016_fall_1">2016秋季学期第一轮选课数据分析报告</a>')
    if request.method == 'POST':
        courses = course_query(request.form['cid'],request.form['cname'],request.form['tname'],'')
        resp = make_response(render_template('querycourse.html',courses=courses))
    elif request.method == 'GET':
        resp = make_response(render_template('querycourse.html',))
    return resp
# @app.route('/card/<func>')
# def cardlogin(func):
#     postData={'username':user,'password':pwd,'url':'http://www.lehu.shu.edu.cn/'}
#     r = s.post('http://passport.lehu.shu.edu.cn/ShowOrgUserInfo.aspx',data=postData,timeout=30)
#     r = s.get('http://card.lehu.shu.edu.cn/CardTradeDetail.aspx',timeout=30)
#     string = r.text
@app.route('/course/<coursename>/<tname>')
def coursepage(coursename, tname):
    course = course_query('', coursename, tname, '')
    if len(course) >= 1:
        resp = make_response(render_template('coursepage.html', course=course[0]))
    else:
        resp = make_response(render_template('coursepage.html', course=course))
    return resp

@app.route('/')
def index():
    flash(randwords())
    resp = make_response(render_template('index.html'))
    return resp


@app.route('/login/<check>/<site>', methods=['POST', 'GET'])#check变量代表此接口是否有验证码site变量代表发生此接口是哪个接口
def login(site, check):
    r = None
    if request.method == 'POST':
        usr = request.form['username']
        pwd = request.form['password']
        if check == 'vali':
            checkcode = request.form['check']
        else:
            checkcode = None
        if '_hash_' in session:
            other = session['_hash_']
        else:
            other = None
        s = cache.get(session[site])
        s = general_login(s, site, usr, pwd, checkcode, other)
        # return s
        if s != False:
            r = getcontent(site, s)
            if r != False:
                cache.set(session[site], s, timeout = 300)
                cache.set(session[site]+'islogin',True,timeout = 300)
                return render_template(site+'.html', r=r)
            else:
                cache.set(session[site]+'islogin',False,timeout = 300)
                flash(u'服务器内容解析出错')
        else:
            if site == 'pe':
                flash(u'如果您的账号密码没填错的话，体育学院服务器又炸啦233...请过一段时间再试试')
            else:
                flash(u'登录失败！可能是账户密码错误或服务器宕机')
            return redirect(url_for('login',site=site,check=check))
    elif request.method == 'GET':
        if site in session and cache.get(session[site]) is not None and cache.get(session[site]+'islogin'):
            s = cache.get(session[site])
            r = getcontent(site, s)
            return render_template(site+'.html', r=r)
        else:
            session[site] = randsession()
            s = requests.Session()
            if check == 'vali':
                r, s, phyhash = getCAPTCHA(site, s)
                if phyhash !=  None:
                    session['_hash_'] = phyhash
            if site == 'pe':
                flash(u'<a class="white-text" href="/aboutpe">关于体育查询的几点说明</a><br/>')
            elif site == 'fin':
                flash(u'请注意！若未修改过密码，初始密码为身份证后六位或学号后六位！！')
            elif site == 'phylab':
                flash(u'请注意！若未修改过密码，初始密码为学号！！')
            cache.set(session[site], s, timeout=300)
            cache.set(session[site] + 'islogin', False, timeout=300)
            resp = make_response(render_template('login.html', r=r,check=(check == 'vali')))
        return resp
    return render_template('index.html')

@app.route('/nhce', methods=['POST', 'GET'])
def nhceroute():
    if request.method == 'POST':
        r = nhce(request.form['username'], request.form['password'], request.form['CID'])
        if r != False:
            resp = make_response(render_template('nhce.html', check=None))
        else:
            resp = make_response(render_template('nhce.html',  check=None))
    elif request.method == 'GET':
        resp = make_response(render_template('nhce.html',check=None))
    return resp

@app.route('/article/<article>')
def articles(article):
    resp = make_response(render_template(article+'.html'))
    return resp
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<tools>')
def tools(tools):
    resp = make_response(render_template(tools+'.html'))
    return resp

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')
