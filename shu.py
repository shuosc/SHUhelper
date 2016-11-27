#! python3
#coding=utf-8
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response
from werkzeug.contrib.cache import SimpleCache
from sqlite3 import dbapi2 as sqlite3
import sys
import string
import re
import requests
import os
import ssl
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

def randsession():
    import random
    import string
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


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
    error = u'<a href="http://shuhelper.cn/article/2016_fall_1">2016秋季学期第一轮选课数据分析报告</a>'
    if request.method == 'POST':
        courses = course_query(request.form['cid'],request.form['cname'],request.form['tname'],'')
        resp = make_response(render_template('querycourse.html',courses=courses,error=error))
    elif request.method == 'GET':
        resp = make_response(render_template('querycourse.html',error=error))
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
    error = u'开学啦~'
    resp = make_response(render_template('index.html', error=error))
    return resp


@app.route('/login/<check>/<site>', methods=['POST', 'GET'])#check变量代表此接口是否有验证码site变量代表发生此接口是哪个接口
def login(site, check):
    error = None
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
                error = u'<a href="/aboutpe">关于体育查询的几点说明</a><br/>'
            elif site == 'fin':
                error = u'请注意！若未修改过密码，初始密码为身份证后六位或学号后六位！！'
            elif site == 'phylab':
                error = u'请注意！若未修改过密码，初始密码为学号！！'
            cache.set(session[site], s, timeout=300)
            cache.set(session[site] + 'islogin', False, timeout=300)
            resp = make_response(render_template('login.html', r=r, error=error, check=(check == 'vali')))
        return resp
    return render_template('index.html', error=error)

@app.route('/nhce', methods=['POST', 'GET'])
def nhceroute():
    if request.method == 'POST':
        r = nhce(request.form['username'], request.form['password'], request.form['CID'])
        if r != False:
            resp = make_response(render_template('nhce.html', error=r, check=None))
        else:
            resp = make_response(render_template('nhce.html', error=u'注册失败！请重新尝试,请注意初始密码为 nhce111', check=None))
    elif request.method == 'GET':
        resp = make_response(render_template('nhce.html', error=u'请注意初始密码为 nhce111', check=None))
    return resp

@app.route('/article/<article>')
def articles(article):
    resp = make_response(render_template(article+'.html'))
    return resp

@app.route('/<tools>')
def tools(tools):
    resp = make_response(render_template(tools+'.html'))
    return resp

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')
