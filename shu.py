#coding=utf-8
from flask import Flask,url_for
from flask import make_response
from flask import request
from flask import render_template
import sys 
import string
import re
import requests
app = Flask(__name__)


def pelogin(user,pwd):
    url='http://202.120.127.149:8989/spims/login.do?method=toLogin'
    postData={'UNumber':user,'Upwd':pwd,'USnumber':u'上海大学'}
    s = requests.Session()
    try:
        r = s.get('http://202.120.127.149:8989/spims/login/index.jsp',timeout=10)
        r = s.post(url,data=postData,timeout=10)
        r = s.get('http://202.120.127.149:8989/spims/exercise.do?method=seacheload',timeout=10)
    except:
        return False
    else:
        table_p=r'<table cellpadding="3" cellspacing="1" class="table_bg">([\s\S]*)<tr>\s+<td colspan="13">'
        content=re.findall(table_p, r.text,re.S|re.M)
        if(len(content)==0):
            return False
        return content[0]

def finlogin(user,pwd):
    url='http://finance.shu.edu.cn/Login.aspx?ReturnUrl=%2fTuition.aspx'
    postData={'__EVENTTARGET':'',
    '__EVENTARGUMENT':'',
    '__VIEWSTATE':'/wEPDwUKLTM3NDg5MjY1NQ9kFgICAQ9kFgICAw9kFhACAQ8PFgIeBFRleHQFNw0KCQkJCQkJCQkJCTxiPueZu+W9leezu+e7nzwvYj7vvIjmnKznp5HmlLbotLnmn6Xor6LvvIlkZAIDDw8WAh4LTmF2aWdhdGVVcmwFNExvZ2luLmFzcHg/UmV0dXJuVXJsPSUyZlR1aXRpb24uYXNweCZFbXBsb3llZUxvZ2luPTFkZAITDw8WAh4HVmlzaWJsZWdkZAIUDw8WBB8ABcQBPGltZyBzcmM9cGljLzEuZ2lmIGJvcmRlcj0wPjxpbWcgc3JjPXBpYy8xLmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvNS5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzUuZ2lmIGJvcmRlcj0wPjxpbWcgc3JjPXBpYy84LmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvNy5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzQuZ2lmIGJvcmRlcj0wPh8CZ2RkAhYPDxYCHwJnZGQCFw8PFgQfAAWoATxpbWcgc3JjPXBpYy81LmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvNS5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzUuZ2lmIGJvcmRlcj0wPjxpbWcgc3JjPXBpYy83LmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvMi5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzQuZ2lmIGJvcmRlcj0wPh8CZ2RkAhkPDxYCHwJnZGQCGw8PFgIfAmdkZGTkUiQcxLjI7qbIyEZc3bENY5Ztjw==',
    '__EVENTVALIDATION':'/wEWBAKXm79JAtXh0pgPAqW0mtsGApOzq+INgXLh/Sj8FgD/gUxZsNSw4Q5MHNc=',
    'login1$txtName':user,
    'login1$txtPsw':pwd,
    'login1$Button1':''}
    s = requests.Session()
    try:
        r = s.post(url,data=postData,timeout=10)
    except:
        return False
    else:
        table_p=r'<table id="Table1" cellspacing="0" cellpadding="0" width="759" align="center" border="0">([\s\S]*)</table>'
        content=re.findall(table_p,r.text,re.S|re.M)
        if(len(content)==0):
            return False
        content=re.findall(table_p,r.text,re.S|re.M)
        string = re.sub(r'<span id="Tuition1_Label2">([\s\S]*)</select>', "", content[0])
        string = re.sub(r"<font color='red'>([\s\S]*?)</font>", "", string)
        return string

def lehulogin(user,pwd):
    postData={'username':user,'password':pwd,'url':'http://www.lehu.shu.edu.cn/'}
    s = requests.Session()
    try:
        r = s.post('http://passport.lehu.shu.edu.cn/ShowOrgUserInfo.aspx',data=postData,timeout=30)
        r = s.get('http://card.lehu.shu.edu.cn/CardTradeDetail.aspx',timeout=30)
    except:
        return False
    else:
        table_p = r'<span id="ctl00_Contentplaceholder1_Label1">([\s\S]*)</form>'
        content = re.findall(table_p,r.text,re.S|re.M)
        if(len(content)==0):
            return False
        else:
            return content[0]
    return False

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    return resp

@app.route('/cal')
def cal():
    resp = make_response(render_template('cal.html'))
    return resp

@app.route('/bus')
def bus():
    resp = make_response(render_template('bus.html'))
    return resp

@app.route('/map')
def map():
    resp = make_response(render_template('map.html'))
    return resp

@app.route('/login/<site>', methods=['POST', 'GET'])
def login(site):
    error = None
    if request.method == 'POST':
        if site == 'pe':
            r = pelogin(request.form['username'],request.form['password'])
        elif site == 'fin':
            r = finlogin(request.form['username'],request.form['password'])
        elif site == 'cardsurplus':
            r = lehulogin(request.form['username'],request.form['password'])
        else:
            r = False
        if r != False:
            return render_template(site+'.html', r=r)
        else:
            error = u'登录失败！可能是账户密码错误或服务器宕机'
            return render_template('index.html', error=error)
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

