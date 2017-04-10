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
        post_data={'UNumber':self.card_id,
        'Upwd':self.password,
        'USnumber':u'上海大学'}
        r = self.session.get(self.url_prefix + '/login/index.jsp',timeout = 30,proxies=self.proxies)
        r = self.session.post(self.url_prefix + '/login.do?method=toLogin',data=post_data, timeout = 30,proxies=self.proxies)
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

class Fin(Client):
    url_prefix = 'http://xssf.shu.edu.cn:8100'
    def __init__(self):
        Client.__init__(self)
        r = self.session.get(self.url_prefix + '/SFP_Share/Home/CheckImgCode',timeout=10,stream=True)
        self.captcha_img = base64.b64encode(r.raw.read()).decode('utf-8')

    def login(self):
        post_data={'userName':self.card_id,
            'pwd':self.password,
            'ktextbox':self.captcha,
            'hidCheckCode':''}
        r = self.session.post(self.url_prefix + '/SFP_Share/?Length=5',data = post_data, timeout=10)
        r = self.session.get(self.url_prefix + '/SFP_Share/', timeout = 10)
        # print(r.text)
        return r.text.find(u'错误') == -1 and r.text.find(u'不正确') == -1

    def get_data(self):
        r = self.session.get(self.url_prefix + '/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_PersonInfo',timeout=10)
        personinfo = re.search(r'(<fieldset([\s\S]*)</fieldset>)',r.text,flags=0).group(0)
        r = self.session.get(self.url_prefix + '/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryPaymentcondition',timeout=10)
        paymentcondition = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        arrearageAmount = re.search(r'[0-9]\d*.[0-9]\d*',r.text,flags=0).group(0)
        personinfo = re.sub(r'<span id="arrearageAmount"></span>',arrearageAmount,personinfo)
        r = self.session.get(self.url_prefix + '/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryChargeRecord',timeout=10)
        chargerecord = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        r = self.session.get(self.url_prefix + '/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryRefundRecord',timeout=10)
        refundrecord = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        content = personinfo+u'<legend></legend><legend>缴费情况</legend>' \
        + paymentcondition+u'<legend>缴费记录</legend>'+chargerecord \
        + u'<legend>退费记录</legend>'+refundrecord+u'<legend></legend>'
        content = re.sub(r'<table class="tblList tblInLine">',\
        '<table class="table  table-striped table-hover table-bordered table-condensed">',content)
        self.data = content
        return True

    def to_json(self):
        return {
            'type':'html',
            'data': self.data
        }

class Lehu(Client):
    url_prefix = 'http://card.lehu.shu.edu.cn'
    def login(self):
        post_data={'username':self.card_id,
        'password':self.password,
        'url':'http://www.lehu.shu.edu.cn/'}
        r = self.session.post('http://passport.lehu.shu.edu.cn/ShowOrgUserInfo.aspx',data = post_data,timeout = 30)
        return r.text != u'1|password|一卡通账号不存在或密码错误！'

    def get_data(self):
        r = self.session.get(self.url_prefix +'/CardTradeDetail.aspx',timeout = 30)
        print(r.text)
        content = re.search(r'<span id="ctl00_Contentplaceholder1_Label1">([\s\S]*)</form>',r.text,flags=0).group(0)
        self.data = content
        return True
    def to_json(self):
        return {
            'type':'html',
            'data': self.data
        }

class XK(Client):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    url_prefix = 'http://xk.shu.edu.cn:8080'
    def __init__(self):
        Client.__init__(self)
        r = self.session.get(self.url_prefix + '/Login/GetValidateCode?GetTimestamp()',timeout=20,stream=True)
        self.captcha_img = base64.b64encode(r.raw.read()).decode('utf-8')

    def login(self):
        post_data = {
            'txtUserName':self.card_id,
            'txtPassword':self.password,
            'txtValiCode':self.captcha}
        print(post_data)
        r = self.session.post(self.url_prefix + '/',data=post_data, headers=self.headers, timeout=60)
        print(r.text)
        # if r.text.find(u'验证码错误') != -1 or r.text.find(u'帐号或密码错误')!=-1 or r.text.find(u'教学评估') != -1:
        return r.text.find('首页')!= -1

    def get_data(self):
        time.sleep(2)
        r = self.session.get(self.url_prefix +'/StudentQuery/CtrlViewQueryCourseTable',timeout=20)
        self.session.get(self.url_prefix + '/Login/Logout')
        string = re.search(r'<table class="tbllist">([\s\S]*?)</table>',r.text,flags=0).group(0)
        self.data = string
        return True

    def to_json(self):
        return {
            'type':'html',
            'data': self.data
        }
