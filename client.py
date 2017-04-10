"""
client class, to simulate a sim client to grab data and preform actions from remote server.
V0.1 2017/04/01 By:cosformula
"""
import base64
import re
import time

import requests
from bs4 import BeautifulSoup

proxiess = None

class Client(object):
    def __init__(self):
        self.card_id = ''
        self.password = ''
        self.captcha_img = ''
        self.captcha = ''
        self.site = ''
        self.subject = ''
        self.session = requests.Session()
        self.data = ''
    def action(self):
        pass
    def verify_user(self):
        pass
    def format_data(self):
        pass
    def get_json(self):
        pass
    def set_account(self, card_id, password, captcha):
        self.card_id = card_id
        self.password = password
        self.captcha = captcha

class Tiyu(Client):
    proxies = None
    url_prefix = 'http://202.120.127.149:8989/spims'
    def login(self):
        self.s = requests.Session()
        postData={'UNumber':self.card_id,
        'Upwd':self.password,
        'USnumber':u'上海大学'}
        r = self.session.get(self.url_prefix + '/login/index.jsp',timeout = 30,proxies=self.proxies)
        r = self.session.post(self.url_prefix + '/login.do?method=toLogin',data=postData, timeout = 30,proxies=self.proxies)
        if(r.headers['Content-Length'] == '784'):
            self.is_login = True
        return True

    def get_data(self):
        r = self.session.get(self.url_prefix + '/exercise.do?method=seacheload',timeout=10,proxies=self.proxies)
        string = r.text
        content=re.search(r'<table cellpadding="3" cellspacing="1" class="table_bg">([\s\S]*)</table>' \
        , string,flags=0).group(0)
        content = re.sub(r'<table cellpadding="3" cellspacing="1" class="table_bg">' \
        , '<table>',content)
        self.data = content
        return True

    def to_json(self):
        return {
            'type':'html',
            'data': self.data
        }


class Services(Client):
    url_prefix = 'http://services.shu.edu.cn'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    def login(self):
        post_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'txtUserName': self.card_id,
            'txtPassword': self.password,
            'btnOk': '提交(Submit)'
        }
        r = self.session.post('http://services.shu.edu.cn/Login.aspx', data=post_data, headers=self.headers)
        if r.text.find('用户名密码错误!') == -1 and r.text.find('系统出错了!') == -1 and r.text.find('工号') == -1:
            return True
        return False

    def get_data(self):
        r = self.session.get(self.url_prefix + '/User/userPerInfo.aspx', timeout=10)
        name = re.search(r'<span id="userName">([\s\S]*?)</span>',r.text,flags=0).group(1)
        nickname = re.search(r'<span id="nickname">([\s\S]*?)</span>',r.text,flags=0).group(1)
        self.data = {
            'name':name,
            'nickname':nickname
        }
        self.session.get(self.url_prefix + '/User/Logout.aspx')
        return True

    def to_json(self):
        return self.data
