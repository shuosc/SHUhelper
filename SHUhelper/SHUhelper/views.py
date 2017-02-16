"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template
from SHUhelper import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response,send_from_directory
from sqlite3 import dbapi2 as sqlite3
from jinja2 import Environment, DictLoader
import sys
import string
import requests
import os
import base64
from SHUhelper.sites import *
from SHUhelper.config import *
import random
import SHUhelper.emptyroom
import SHUhelper.forms
import SHUhelper.schooltime 
import SHUhelper.findfreetime
from SHUhelper.models import db, Comment, User, Words,Students
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import login_user
import flask_login
import flask_admin 
from flask_admin import helpers, expose
class SHUModelView(ModelView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('ulogin', next=request.url))
class SHUFileAdmin(FileAdmin):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('ulogin', next=request.url))

admin = Admin(app, name='SHUhelper', template_mode='bootstrap3')
admin.add_view(SHUModelView(User, db.session))
admin.add_view(SHUModelView(Comment, db.session))
admin.add_view(SHUModelView(Words, db.session))
admin.add_view(SHUModelView(Students, db.session))
path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(SHUFileAdmin(path, '/static/', name='Static Files'))

@app.route('/ulogin', methods=['POST', 'GET'])
def ulogin():
    from SHUhelper.forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, False)
            return redirect(request.args.get('next') or url_for('admin.index'))
        flash('Invalid username or password','card')
    return render_template('ulogin.html', form=form)

def randsession():
    """生成随机sessoin"""
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
    """数据库查询接口"""
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
def query_course():
    """查询课程逻辑"""
    flash(u'<a class="white-text" href="http://shuhelper.cn/article/2016_fall_1">2016秋季学期第一轮选课数据分析报告</a>','card')
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
def course_page(coursename, tname):
    course = course_query('', coursename, tname, '')
    if len(course) >= 1:
        resp = make_response(render_template('coursepage.html', course=course[0]))
    else:
        resp = make_response(render_template('coursepage.html', course=course))
    return resp

@app.route('/', methods=['POST', 'GET'])
def index():
    DAILY_WORDS = Words.query.filter_by(visible=True).all()
    comment = None
    form = SHUhelper.forms.CommentForm()
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(postid='index',
                          username=form.username.data,
                          comment=form.comment.data,
                          time=datetime.now())
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('index'))
    flash(random.choice(DAILY_WORDS).content,'card')
    flash('#欢迎关注我们的微信公众号 搜索:shuhelper','toast')
    comments = Comment.query.filter_by(postid='index').order_by(Comment.id.desc()).all()
    resp = make_response(render_template('index.html', form=form,comments=comments))
    return resp


@app.route('/findfreetime/member', methods=['POST', 'GET'])
def findfreetime_member():
    r = None 
    site = 'fft'
    check = 'vali'
    if request.method == 'POST':
        week = int(request.form['week'])
        code = request.form['code']
        usr = request.form['username']

        pwd = request.form['password']
        check_code = request.form['check']
        s = CACHE.get(session[site])
        student = Students(students_id=usr,
                           login_site='findfreetime',
                           time=datetime.now())
        db.session.add(student)
        db.session.commit()
        status,s = general_login(s, 'xkc', usr, pwd, check_code, None)
        if status == 'success':
            r = get_content('xkc', s)
            if r != False:
                if CACHE.get(code) is None:
                    members=set()
                    members.add(usr)
                    CACHE.set(code,members,timeout = 500)
                else:
                    members = set(CACHE.get(code))
                    members.add(usr)
                    CACHE.set(code,members,timeout = 500)
                flash(u'您已以%s的身份在%s小组中成功录入课表' % (usr,code),'card')
                flash(u'若您是组织者，请点击<a href="/findfreetime/answer" class="waves-effect waves-light btn">这里</a>查看结果','card')
                CACHE.set(session[site], s, timeout = 500)
                CACHE.set(session[site]+'user', usr, timeout = 500)
                time_list = SHUhelper.findfreetime.get_binary_json_from_course_table(r,week)
                CACHE.set(code+usr, time_list, timeout = 500)
                CACHE.set(session[site]+'islogin',True,timeout = 500)
                return render_template('xkc.html', r=r)
            else:
                CACHE.set(session[site]+'islogin',False,timeout = 500)
                flash(u'服务器内容解析出错','card')
        elif status =='error_vali':
            flash(u'验证码错误','card')
        elif status =='error_pwd':
            flash(u'用户名或密码错误','card')
        elif status =='error_cj':
            flash(u'您尚未完全完成教学评估！\n在浏览器中打开<a href="http://cj.shu.edu.cn" class="white-text"> http://cj.shu.edu.cn </a> 转至教学评估网站。请注意军事技能或军事理论是否评估','card')
        else:
            flash(u'登录失败！可能是账户密码错误或服务器宕机','card')
        return redirect(url_for('findfreetime_member'))
    elif request.method == 'GET':
        flash(u'和组员输入同样的数字(建议五位),进入同一个小组','card')
        session[site] = randsession()
        while CACHE.get(session[site]) is not None:
            session[site] = randsession()
        s = requests.Session()
        r, s, phy_hash = get_CAPTCHA('xkc',s)
        CACHE.set(session[site], s, timeout=500)
        CACHE.set(session[site] + 'islogin', False, timeout=500)
        resp = make_response(render_template('findfreetime_login.html', r=r,check=(check == 'vali')))
        return resp
    return render_template('findfreetime_login.html')

@app.route('/findfreetime/answer', methods=['POST', 'GET'])
def findfreetime_answer():
    if request.method == 'POST':
        code = request.form['code']
        data = []
        if CACHE.get(code) is not None:
            for members in CACHE.get(code):
                data.append(CACHE.get(code+members))
            count = len(CACHE.get(code))
            raw_list =  SHUhelper.findfreetime.detect_conflict(data)
            Traverse_list = [([1] * 5) for i in range(0,13)]
            for j in range(0,5):
                for i in range(0,13):
                    Traverse_list[i][j]=raw_list[j][i]
            return render_template('findfreetime_answer.html',code=code,r=Traverse_list,count=count)
        else:
            flash(u'还没有任何人将课表录入您输入的小组代码，请检查小组代码是否有误','card')
            return render_template('findfreetime_code.html')
    elif request.method == 'GET':
        flash(u'输入组织代码查看结果','card')
        return render_template('findfreetime_code.html')
    

@app.route('/findemptyroom', methods=['POST', 'GET'])
def findemptyroom():
    classrooms = []
    if request.method == 'POST':
        week = int(request.form['week'])
        day = int(request.form['day'])
        time = int(request.form['time'])
        classrooms = SHUhelper.emptyroom.get_emptyroom(week,day,time)
        flash(u'您当前输入的查询参数是，第%d周，星期%d，第%d节'% (week, day, time),'card')
        return make_response(render_template('findemptyroom.html' ,classrooms = classrooms, status = u"您查询的时间"))

    elif request.method == 'GET':
        week = SHUhelper.schooltime.this_week()
        day = SHUhelper.schooltime.this_day()
        time = SHUhelper.schooltime.this_class()
        flash(u'当前时间是，第%d周，星期%d，第%d节'% (week, day, time),'card')
        classrooms = SHUhelper.emptyroom.get_emptyroom_now()
        return make_response(render_template('findemptyroom.html' ,classrooms = classrooms, status = u"现在的"))
    return make_response(render_template('findemptyroom.html'))


@app.route('/login/<check>/<site>', methods=['POST', 'GET'])#check变量代表此接口是否有验证码site变量代表发生此接口是哪个接口
def login(site, check):
    r = None
    if request.method == 'POST':
        usr = request.form['username']
        pwd = request.form['password']
        if usr == 'angelina':
            return 'mdzz'
        try:
            int(usr)
        except:
            flash('登录失败！可能是账户密码错误或服务器宕机','card')
            return redirect(url_for('login',site=site,check=check))
            
        student = Students(students_id=usr,
                           login_site=site,
                           time=datetime.now())
        db.session.add(student)
        db.session.commit()

        if usr == '15121604':
            flash('欢迎尊贵的SHUhelper SVIP登录','toast')
        if usr == '15122265':
            flash('欢迎钱爸爸登录，耶','toast')
        if usr == '15120993':
            flash('欢迎伟龙爸爸登录','toast')
        if usr =='16122415':
            flash('欢迎佩瑶女儿登录','toast')
        if usr =='16122622':
            flash('欢迎佩璇女儿登录','toast')
        if check == 'vali':
            check_code = request.form['check']
        else:
            check_code = None
        if '_hash_' in session:
            other = session['_hash_']
        else:
            other = None
        status,s = general_login(CACHE.get(session[site]), site, usr, pwd, check_code, other)
        if status == 'success':
            r = get_content(site, s)
            if r != False:
                CACHE.set(session[site]+'content',r,timeout=300)
                CACHE.set(session[site], s, timeout = 300)
                CACHE.set(session[site]+'islogin',True,timeout = 300)
                return render_template(site+'.html', r=r)
            else:
                CACHE.set(session[site]+'islogin',False,timeout = 300)
                flash(u'服务器内容解析出错','card')
        elif status == 'error_vali':
                flash(u'验证码错误！','card')
        elif status =='error_pwd':
            flash(u'用户名或密码错误','card')
        else:
            if site == 'pe':
                flash(u'如果您的账号密码没填错的话，体育学院服务器又炸啦233...请过一段时间再试试','toast')
            else:
                flash(u'登录失败！可能是账户密码错误或服务器宕机','card')
        return redirect(url_for('login',site=site,check=check))
    elif request.method == 'GET':
        if site in session and CACHE.get(session[site]) is not None and CACHE.get(session[site]+'islogin'):
            s = CACHE.get(session[site])
            r = CACHE.get(session[site]+'content')
            #r = get_content(site, s)
            return render_template(site+'.html', r=r)
        else:
            session[site] = randsession()
            while CACHE.get(session[site]) is not None:
                session[site] = randsession()
            s = requests.Session()
            if check == 'vali':
                r, s, phy_hash = get_CAPTCHA(site,s)
                if phy_hash !=  None:
                    session['_hash_'] = phy_hash
            if site == 'pe':
                flash(u'<a class="white-text" href="/aboutpe">关于体育查询的几点说明</a><br/>','card')
            elif site == 'fin':
                flash(u'请注意！若未修改过密码，初始密码为身份证后六位或学号后六位！！','card')
            elif site == 'phylab':
                flash(u'请注意！若未修改过密码，初始密码为学号！！','card')
            elif site == 'cj':
                flash(u'请注意！登录炒鸡慢，要等将近四十秒。','card')
            CACHE.set(session[site], s, timeout=300)
            CACHE.set(session[site] + 'islogin', False, timeout=300)
            resp = make_response(render_template('login.html', r=r,check=(check == 'vali' or check =='valia')))
        return resp
    return render_template('index.html')

@app.route('/nhce', methods=['POST', 'GET'])
def nhce_route():
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

@app.route('/baidu-verify-536C3DC984.txt')
def verify():
    return '85c04123f2acd58ef6a067543f20d359'

@app.route('/12500000001.txt')
def tverify():
    return 'hello'