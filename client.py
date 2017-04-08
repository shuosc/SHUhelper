"""
client class, to simulate a sim client to grab data from remote server.
V0.1 2017/04/01 By:cosformula
"""
import requests
import re
from bs4 import BeautifulSoup
import base64
import time

POST_DATA = {
    'xk':'',
}

proxiess = None

class Client(object):
    def __init__(self):
        self.card_id = ''
        self.password = ''
        self.captcha_img = ''
        self.captcha = ''
        self.extra_hash = ''
        self.site = ''
        self.subject = ''
        self.is_login = False
        self.is_data_get = False
        self.s = requests.Session()
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
    url_prefix = 'http://202.120.127.149:8989/spims'
    def login(self):
        postData={'UNumber':self.card_id,
        'Upwd':self.password,
        'USnumber':u'上海大学'}
        r = self.s.get(self.url_prefix + '/login/index.jsp',timeout = 30,proxies=proxies)
        r = self.s.post(self.url_prefix + '/login.do?method=toLogin',data=postData, timeout = 30,proxies=proxies)
        if(r.headers['Content-Length'] == '784'):
            self.is_login = True
        return True

    def get_data(self):
        r = self.s.get(self.url_prefix + '/exercise.do?method=seacheload',timeout=10,proxies=proxies)
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
    def login(self):
        r = self.s.get(self.url_prefix + '/Login.aspx')
        view_state = re.search(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([\s\S]*)" />',r.text,flags=0).group(1)
        post_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': view_state,
            'txtUserName': self.card_id,
            'txtPassword': self.password,
            'btnOk': '提交(Submit)'
        }
        r = self.s.post(self.url_prefix + '/Login.aspx', data=post_data)
        if r.text.find('用户名密码错误!') == -1 :
            self.is_login = True
        return True

    def get_data(self):
        r = self.s.get(self.url_prefix + '/User/userPerInfo.aspx')
        name = re.search(r'<span id="userName">([\s\S]*?)</span>',r.text,flags=0).group(1)
        nickname = re.search(r'<span id="nickname">([\s\S]*?)</span>',r.text,flags=0).group(1)
        self.data = {
            'name':name,
            'nickname':nickname
        }
        self.is_data_get = True
        self.s.get(self.url_prefix + '/User/Logout.aspx')

    def to_json(self):
        return self.data
