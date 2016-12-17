#!/usr/bin/env python3
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
from config import *
import random
import emptyroom
import schooltime
import findfreetime
cache = SimpleCache()

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
def course_page(coursename, tname):
    course = course_query('', coursename, tname, '')
    if len(course) >= 1:
        resp = make_response(render_template('coursepage.html', course=course[0]))
    else:
        resp = make_response(render_template('coursepage.html', course=course))
    return resp

@app.route('/')
def index():
    flash(random.choice(DAILY_WORDS))
    resp = make_response(render_template('index.html'))
    return resp

# @app.route('/findfreetime', methods=['POST', 'GET'])
# def findfreetime_index():
#     time_lists = []
#     if request.method == 'POST':
#         for studentno in request.form['studentno']:
#             if(cache.get(studentno) is None):
#                 # flash(u'学号为%s的同学五分钟内未在本系统查询过课表，本次查询失败')
#             else:
#                 time_lists.append(cache.get(studentno))
#         solution = detect_conflict(time_lists)
#         return make_response(render_template('findfreetime.html'), r = solution)
#     elif request.method == 'GET':
#         return make_response(render_template('findfreetime.html'))
#     return make_response(render_template('findfreetime.html'))


@app.route('/findfreetime/member', methods=['POST', 'GET'])
def findfreetime_member():
    r = None 
    site = 'fft'
    check = 'vali'
    if request.method == 'POST':
        week = int(request.form['week'])
        code = request.form['code']
        usr = request.form['username']
        if usr == '15122265' or usr == '15121604':
            flash(u'钱宜文炒鸡可爱')
            pass
        pwd = request.form['password']
        check_code = request.form['check']
        s = cache.get(session[site])
        status,s = general_login(s, 'xkc', usr, pwd, check_code, None)
        if status == True:
            r = get_content('xkc', s)
            if r != False:
                if cache.get(code) is None:
                    members=set()
                    members.add(usr)
                    cache.set(code,members,timeout = 500)
                else:
                    members = set(cache.get(code))
                    members.add(usr)
                    cache.set(code,members,timeout = 500)
                    flash(u"测试代码")
                flash(u'您已以%s的身份在%s小组中成功录入课表' % (usr,code))
                flash(u'若您是组织者，请点击<a href="/findfreetime/answer" class="waves-effect waves-light btn">这里</a>查看结果')
                cache.set(session[site], s, timeout = 500)
                cache.set(session[site]+'user', usr, timeout = 500)
                time_list = findfreetime.get_binary_json_from_course_table(r,week)
                cache.set(code+usr, time_list, timeout = 500)
                cache.set(session[site]+'islogin',True,timeout = 500)
                return render_template('xkc.html', r=r)
            else:
                cache.set(session[site]+'islogin',False,timeout = 500)
                flash(u'服务器内容解析出错')
                flash(r)
        elif status =='error_vali':
            flash(u'验证码错误')
        elif status =='error_pwd':
            flash(u'用户名或密码错误')
        else:
            flash(u'登录失败！可能是账户密码错误或服务器宕机')
        return redirect(url_for('findfreetime_member'))
    elif request.method == 'GET':
        flash(u'和组员输入同样的数字(建议五位),进入同一个小组')
        session[site] = randsession()
        while cache.get(session[site]) is not None:
            session[site] = randsession()
        s = requests.Session()
        r, s, phy_hash = get_CAPTCHA('xkc',s)
        cache.set(session[site], s, timeout=500)
        cache.set(session[site] + 'islogin', False, timeout=500)
        resp = make_response(render_template('findfreetime_login.html', r=r,check=(check == 'vali')))
        return resp
    return render_template('findfreetime_login.html')

@app.route('/findfreetime/answer', methods=['POST', 'GET'])
def findfreetime_answer():
    if request.method == 'POST':
        code = request.form['code']
        data = []
        if cache.get(code) is not None:
            for members in cache.get(code):
                data.append(cache.get(code+members))
            count = len(cache.get(code))
            raw_list =  findfreetime.detect_conflict(data)
            Traverse_list = [([1] * 5) for i in range(0,13)]
            for j in range(0,5):
                for i in range(0,13):
                    Traverse_list[i][j]=raw_list[j][i]
            return render_template('findfreetime_answer.html',code=code,r=Traverse_list,count=count)
        else:
            flash(u'还没有任何人将课表录入您输入的小组代码，请检查小组代码是否有误')
            return render_template('findfreetime_code.html')
    elif request.method == 'GET':
        flash(u'输入组织代码查看结果')
        return render_template('findfreetime_code.html')
    

@app.route('/findemptyroom', methods=['POST', 'GET'])
def findemptyroom():
    classrooms = []
    if request.method == 'POST':
        week = int(request.form['week'])
        day = int(request.form['day'])
        time = int(request.form['time'])
        classrooms = emptyroom.get_emptyroom(week,day,time)
        flash(u'您当前输入的查询参数是，第%d周，星期%d，第%d节'% (week, day, time))
        return make_response(render_template('findemptyroom.html' ,classrooms = classrooms, status = u"您查询的时间"))

    elif request.method == 'GET':
        week = schooltime.this_week()
        day = schooltime.this_day()
        time = schooltime.this_class()
        flash(u'当前时间是，第%d周，星期%d，第%d节'% (week, day, time))
        classrooms = emptyroom.get_emptyroom_now()
        return make_response(render_template('findemptyroom.html' ,classrooms = classrooms, status = u"现在的"))
    return make_response(render_template('findemptyroom.html'))


@app.route('/login/<check>/<site>', methods=['POST', 'GET'])#check变量代表此接口是否有验证码site变量代表发生此接口是哪个接口
def login(site, check):
    r = None
    if request.method == 'POST':
        usr = request.form['username']
        if usr == '15122265' or usr == '15121604':
            flash(u'钱宜文炒鸡可爱')
        pwd = request.form['password']
        if check == 'vali':
            check_code = request.form['check']
        else:
            check_code = None
        if '_hash_' in session:
            other = session['_hash_']
        else:
            other = None
        status,s = general_login(cache.get(session[site]), site, usr, pwd, check_code, other)
        if status == True:
            r = get_content(site, s)
            if r != False:
                cache.set(session[site], s, timeout = 300)
                cache.set(session[site]+'islogin',True,timeout = 300)
                return render_template(site+'.html', r=r)
            else:
                cache.set(session[site]+'islogin',False,timeout = 300)
                flash(u'服务器内容解析出错')
        elif status == 'error_vali':
                flash(u'验证码错误！')
        elif status =='error_pwd':
            flash(u'用户名或密码错误')
        else:
            if site == 'pe':
                flash(u'如果您的账号密码没填错的话，体育学院服务器又炸啦233...请过一段时间再试试')
            else:
                flash(u'登录失败！可能是账户密码错误或服务器宕机')
        return redirect(url_for('login',site=site,check=check))
    elif request.method == 'GET':
        if site in session and cache.get(session[site]) is not None and cache.get(session[site]+'islogin'):
            s = cache.get(session[site])
            r = get_content(site, s)
            return render_template(site+'.html', r=r)
        else:
            session[site] = randsession()
            while cache.get(session[site]) is not None:
                session[site] = randsession()
            s = requests.Session()
            if check == 'vali':
                r, s, phy_hash = get_CAPTCHA(site,s)
                if phy_hash !=  None:
                    session['_hash_'] = phy_hash
            if site == 'pe':
                flash(u'<a class="white-text" href="/aboutpe">关于体育查询的几点说明</a><br/>')
            elif site == 'fin':
                flash(u'请注意！若未修改过密码，初始密码为身份证后六位或学号后六位！！')
            elif site == 'phylab':
                flash(u'请注意！若未修改过密码，初始密码为学号！！')
            elif site == 'cj':
                flash(u'请注意！登录炒鸡慢，要等将近四十秒。')
            cache.set(session[site], s, timeout=300)
            cache.set(session[site] + 'islogin', False, timeout=300)
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

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
