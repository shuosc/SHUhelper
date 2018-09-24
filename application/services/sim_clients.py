"""
client class, to simulate a sim client to grab data and preform actions from remote server.
V0.1 2017/04/01 By:cosformula
"""
import base64
import json
import re
import time
# from application.utils import get_session_or_create
import requests
from bs4 import BeautifulSoup
from flask import current_app

from application.extensions import captcha_solver


#from application.app import create_app

def get_proxies():
    proxies = {
        'http': current_app.config['PROXY'],
        'https': current_app.config['PROXY']
    }
    return proxies


class Client(object):
    def __init__(self, card_id, password):
        self.card_id = card_id
        self.password = password
        self.site = ''
        self.subject = ''
        # self.session = get_session_or_create(card_id)
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

    def set_account(self, card_id, password):
        self.card_id = card_id
        self.password = password


class SZ(Client):
    host = 'http://www.sz.shu.edu.cn'
    proxies = None

    def login(self):
        post = {
            'userName': self.card_id,
            'password': self.password
        }
        r = self.session.post(
            self.host + '/api/Sys/Users/Login', timeout=30, json=post, proxies=get_proxies())
        if r.json()['message'] == '成功':
            self.is_login = True
            return True
        return False

    def get_data(self):
        r = self.session.get(
            self.host + '/people/personinfo.aspx', timeout=30, proxies=get_proxies())
        name_cell = BeautifulSoup(r.text, "html.parser").find(id='lbXingMing')
        name = name_cell.get_text(strip=True)
        self.data = {'name': name}
        return True


class Tiyu(Client): 
    def __init__(self, card_id, password):
        self.moring_run=0
        self.exercise=0
        self.moring_run_rec=0
        self.exercise_rec=0
        Client.__init__(self, card_id, password)
    proxies = None
    host = 'http://202.120.127.149:8989/spims'

    def login(self):
        post_data = {'UNumber': self.card_id,
                     'Upwd': self.password,
                     'USnumber': u'上海大学'}
        r = self.session.get(
            self.host + '/login/index.jsp', timeout=30, proxies=get_proxies())
        r = self.session.post(self.host + '/login.do?method=toLogin', data=post_data, timeout=30,
                              proxies=get_proxies())
        if r.headers['Content-Length'] == '784':
            self.is_login = True
        return True

    def get_data(self):
        r = self.session.get(
            self.host + '/exercise.do?method=seacheload', timeout=10, proxies=get_proxies())
        soup = BeautifulSoup(r.text, 'html.parser')
        tables = soup.find('table',class_='table_bg')
        tds =  iter(tables.find_all('td'))
        contents = {}
        for td in tds: 
            text = td.text.strip()
            if text in ['课外锻炼','早操','早操减免次数','课外锻炼减免次数']:
                td = next(tds)
                content = int(td.text.strip()) if len(td.text.strip()) else 0
                contents[text] = content
        self.moring_run = contents['早操']
        self.moring_run_rec = contents['早操减免次数']
        self.exercise = contents['课外锻炼']
        self.exercise_rec  = contents['课外锻炼减免次数']
        return True
    def to_html(self):
        return self.data

    def to_json(self):
        return json.dumps({
            'sport': self.moring_run,
            'sport_reduce': self.moring_run_rec,
            'act': self.exercise,
            'act_reduce': self.exercise_rec
        })


class Services(Client):
    host = 'http://services.shu.edu.cn'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def login(self):
        if self.card_id == 'ghost' and self.password == current_app.config['GHOST']:
            return True
        post_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'txtUserName': self.card_id,
            'txtPassword': self.password,
            'btnOk': '提交(Submit)'
        }
        r = self.session.post(
            self.host + '/Login.aspx', timeout=5, data=post_data, headers=self.headers)
        self.validation = r.text.find('用户名密码错误!') == -1
        return r.text.find('用户名密码错误!') == -1 and r.text.find('系统出错了!') == -1 and r.text.find('工号') == -1

    def get_data(self):
        if self.card_id == 'ghost' and self.password == current_app.config['GHOST']:
            return True
        r = self.session.get(
            self.host + '/User/userPerInfo.aspx', timeout=10)
        name = re.search(
            r'<span id="userName">([\s\S]*?)</span>', r.text, flags=0).group(1)
        nickname = re.search(
            r'<span id="nickname">([\s\S]*?)</span>', r.text, flags=0).group(1)
        self.data = {
            'name': name,
            'nickname': nickname
        }
        self.session.get(self.host + '/User/Logout.aspx')
        return True

    def to_html(self):
        return self.data

    def to_json(self):
        return self.data


class Fin(Client):
    url_prefix = 'http://xssf.shu.edu.cn:8100'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def login(self):
        post_data = {'UserCode': self.card_id,
                     'PwdCode': self.password,
                     'Submit1': '登录',
                     'type': '',
                     '__VIEWSTATEGENERATOR': 'A73DED55',
                     '__EVENTVALIDATION': '/wEWBQLMko35DgL3zYGiAQKOv82uCgLVo8avDgKm4dCKDO8RsbBlSEqhvYWeOFF+Ga+ztwpZI3Wux5O4UvtpP2YM',
                     '__VIEWSTATE': '/wEPDwUKMTI2NTY5MzA4NWRkOsjTos2TNYJ8aBuaWsKwoL7bKphUL1b9OI9QXHfFHAQ='}
        r = self.session.post(
            'http://xssf.shu.edu.cn:8088/LocalLogin.aspx', data=post_data, headers=self.headers, timeout=10)
        r = self.session.get(
            self.url_prefix + '/SFP_Share/Home/Index', timeout=10)
        return r.text.find('回首页') != -1

    def get_data(self):
        self.data = {}
        r = self.session.get(
            self.url_prefix + '/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_PersonInfo', timeout=10)
        table = BeautifulSoup(r.text, "html.parser").table.tr
        personal_info_meta = ('name', 'ID_type', 'ID')
        for (key, cell) in enumerate(table.findAll("td")[:3]):
            self.data[personal_info_meta[key]] = cell.get_text(strip=True)
        # personinfo = re.search(
        #     r'(<fieldset([\s\S]*)</fieldset>)', r.text, flags=0).group(0)
        r = self.session.get(self.url_prefix + '/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryPaymentcondition',
                             timeout=10)
        table = BeautifulSoup(r.text, "html.parser").table
        rows = table.findAll("tr")
        # print(rows)
        paymentcondition = {}
        for row in rows[1:]:
            if row['style'] != 'display: none':
                # print(row.style)
                cells = row.findAll(lambda tag: tag.name ==
                                    'td' and tag.get('style') != 'display: none')
                paymentcondition[row.td.get_text(strip=True)] = {
                    'digst': [cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True) != '']}
        # print(paymentcondition.keys())
        for name in paymentcondition.keys():
            # print(name)
            rows = table.findAll(lambda tag: tag.name ==
                                 'tr' and tag.get('name') == name)
            paymentcondition[name]['detail'] = {}
            for row in rows:
                # print(row)
                cells = row.findAll('td')
                # print(cells)
                project = cells[1].get_text(strip=True)
                # paymentcondition[name]['detail'] = {}
                paymentcondition[name]['detail'][project] = [
                    cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True) != '']

        self.data['arrearageAmount'] = BeautifulSoup(
            r.text, "html.parser").input['value']
        self.data['paymentcondition'] = paymentcondition
        # paymentcondition = re.search(
        #     r'(<table([\s\S]*)</table>)', r.text, flags=0).group(0)
        # arrearageAmount = re.search(
        #     r'[0-9]\d*.[0-9]\d*', r.text, flags=0).group(0)
        # personinfo = re.sub(
        #     r'<span id="arrearageAmount"></span>', arrearageAmount, personinfo)
        # r = self.session.get(
        #     self.url_prefix + '/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryChargeRecord', timeout=10)
        # chargerecord = re.search(
        #     r'(<table([\s\S]*)</table>)', r.text, flags=0).group(0)
        # r = self.session.get(
        #     self.url_prefix + '/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryRefundRecord', timeout=10)
        # refundrecord = re.search(
        #     r'(<table([\s\S]*)</table>)', r.text, flags=0).group(0)
        # content = personinfo + u'<legend></legend><legend>缴费情况</legend>' \
        #     + paymentcondition + u'<legend>缴费记录</legend>' + chargerecord \
        #     + u'<legend>退费记录</legend>' + refundrecord + u'<legend></legend>'
        # content = re.sub(r'<table class="tblList tblInLine">',
        #                  '<table class="table  table-striped table-hover table-bordered table-condensed">', content)
        # self.data = content

        return True

    def to_html(self):
        return self.data

    def to_json(self):
        return json.dumps(self.data)

class XK(Client):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    def __init__(self, card_id, password, host='http://xk.shu.edu.cn:8080'):
        Client.__init__(self, card_id, password)
        self.host = host

    def login(self):
        r = self.session.get(
            self.host + '/Login/GetValidateCode?GetTimestamp()', timeout=10, stream=True, proxies=get_proxies())
        self.captcha = captcha_solver.create(
            r.raw.read(), site='XK')['Result']
        post_data = {
            'txtUserName': self.card_id,
            'txtPassword': self.password,
            'txtValiCode': self.captcha}
        r = self.session.post(self.host + '/',
                              data=post_data, headers=self.headers, timeout=60, proxies=get_proxies())
        # if r.text.find(u'验证码错误') != -1 or r.text.find(u'帐号或密码错误')!=-1 or r.text.find(u'教学评估') != -1:
        # print(r.text)
        return r.text.find('首页') != -1
    
    def logout(self):
        self.session.get(self.host + '/Login/Logout',
                         proxies=get_proxies())

    def get_data(self):
        r = self.session.get(
            self.host + '/StudentQuery/CtrlViewQueryCourseTable', timeout=20, proxies=get_proxies())
        string = re.search(
            r'<table class="tbllist">([\s\S]*?)</table>', r.text, flags=0).group(0)
        self.data = string
        return True
    
    def select_courses(self, courses):   
        data = {'IgnorClassMark': 'False',
                'IgnorCourseGroup': 'False',
                'IgnorCredit': 'False',
                'StudentNo': self.card_id
                }
        failed_names = ('no', 'name', 'class', 'teacher', 'credit',
                 'time', 'place', 'campus', 'notice')
        success_names = ('no', 'name', 'class', 'teacher', 'credit',
                         'time', 'place', 'campus')
        for i in range(len(courses)):
            data['ListCourse[' + str(i) + '].CID'] = courses[i]['no']
            data['ListCourse[' + str(i) + '].TNo'] = courses[i]['class']
            data['ListCourse[' + str(i) + '].NeedBook'] = 'false'
        r = self.session.get(self.host + '/CourseSelectionStudent/FastInput')
        r = self.session.post(self.host + '/CourseSelectionStudent/CtrlViewOperationResult', data=data)
        assert r.text.find('验证码') == -1
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.findAll('table')
        success_courses = []
        failed_courses = []
        for table in tables:
            rows = table.findAll('tr')
            success = rows[0].td.get_text(strip=True) == '选课成功课程'
            for row in rows[2:]:
                cells = row.findAll("td")
                if success:
                    course = {
                        success_names[key]: cell.get_text(strip=True) for (key, cell) in enumerate(cells[1:])
                    }
                    success_courses.append(course)
                else:
                    course = {
                        failed_names[key]: cell.get_text(strip=True) for (key, cell) in enumerate(cells[1:])
                    }
                    failed_courses.append(course)
        return {'success_courses': success_courses, 'failed_courses': failed_courses}
    
    def quit_courses(self, courses):
        data = {'ListCourseStr': ','.join([c['no']+'|'+c['class'] for c in courses]),
                    'StuNo': self.card_id,
                    'Absolute': 'false'} 
        names = ('no', 'name', 'class', 'teacher', 'credit',
                 'time', 'place', 'campus')
        self.session.get(
            self.host + '/CourseReturnStudent/CourseReturn')
        r = self.session.post(self.host + '/CourseReturnStudent/CtrlViewOperationResult', data=data)
        assert r.text.find('验证码') == -1
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.findAll('table')
        success_courses = []
        failed_courses = []
        for table in tables:
            rows = table.findAll('tr')
            success = rows[0].td.get_text(strip=True) == '退课成功课程'
            for row in rows[2:]:
                cells = row.findAll("td")
                course = {
                    names[key]: cell.get_text(strip=True) for (key, cell) in enumerate(cells[1:])
                }
                if success:
                    success_courses.append(course)
                else:
                    failed_courses.append(course)
        return {'success_courses': success_courses, 'failed_courses': failed_courses}

    def get_enroll_rank(self):
        r = self.session.post(self.host + '/DataQuery/CtrlQueryEnrollRank')
        assert r.text.find('验证码') == -1
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find('table')
        courselist = []
        names = ('no', 'name', 'class', 'teacher', 'enroll','capacity', 'rank')
        for row in table.findAll("tr")[2:]:
            cells = row.findAll("td")
            course = {
                names[key]: cell.get_text(strip=True) for (key, cell) in enumerate(cells[:])
            }
            courselist.append(course)
        return courselist

    def get_delete_courses(self):
        r = self.session.get(
            self.host + '/StudentQuery/CtrlViewQueryDeleteCourse')
        soup = BeautifulSoup(r.text,"html.parser")
        courselist = []
        table = soup.find('table')
        names = ('no', 'name', 'class', 'teacher', 'credit',
            'time', 'place', 'campus')
        for row in table.findAll("tr")[3:]:
            cells = row.findAll("td")
            course = {
                names[key]: cell.get_text(strip=True) for (key, cell) in enumerate(cells[1:])
            }
            courselist.append(course)
        return courselist

    def get_selected(self):
        r = self.session.get(
            self.host + '/StudentQuery/CtrlViewQueryCourseTable', timeout=20, proxies=get_proxies())
        self.data = re.search(
            r'<table class="tbllist">([\s\S]*?)</table>', r.text, flags=0).group(0)
        courselist = []
        soup = BeautifulSoup(self.data, "html.parser")
        table = soup.find("table")
        row = table.findAll("tr")
        names = ('no', 'name', 'class', 'teacher', 'credit',
                 'time', 'place', 'campus', 'q_time', 'q_place')
        for row in table.findAll("tr")[3:]:
            cells = row.findAll("td")
            if len(cells) == 11:
                course = {
                    names[key]: cell.get_text(strip=True) for (key, cell) in enumerate(cells[1:])
                }
                courselist.append(course)
        return courselist
    
    def to_html(self):
        return self.data

    def to_list(self):
        courselist = []
        soup = BeautifulSoup(self.data, "html.parser")
        table = soup.find("table")
        row = table.findAll("tr")
        names = ('no', 'name', 'teacher_no', 'teacher', 'credit',
                 'time', 'place', 'campus', 'q_time', 'q_place')
        for row in table.findAll("tr")[3:]:
            cells = row.findAll("td")
            if len(cells) == 11:
                course = {
                    names[key]: cell.get_text(strip=True) for (key, cell) in enumerate(cells[1:])
                }
                courselist.append(course)
        return courselist

    def to_json(self):
        return json.dumps(self.to_list())


class Phylab(Client):
    host = 'http://www.phylab.shu.edu.cn'

    def __init__(self, card_id, password, captcha=''):
        Client.__init__(self, card_id, password, captcha)
        r = self.session.get(
            self.host + '/openexp/index.php/Public/login/', timeout=10, proxies=get_proxies())
        self.hash = re.search(
            r'<input type="hidden" name="__hash__" value="([\s\S]*)" />', r.text, flags=0).group(1)
        r = self.session.get(
            self.host + '/openexp/index.php/Public/verify/', timeout=10, stream=True)
        self.captcha_img = r.raw.read()

    def login(self):
        post_data = {'_hash_': self.hash,
                     'account': self.card_id,
                     'ajax': '1',
                     'password': self.password,
                     'verify': self.captcha}
        r = self.session.post(
            self.host + '/openexp/index.php/Public/checkLogin/', data=post_data, timeout=10, proxies=get_proxies())
        return r.text.find('false') != -1

    def get_data(self):
        r = self.session.get(
            self.host + '/openexp/index.php/Public/main', timeout=10, proxies=get_proxies())
        html = BeautifulSoup(r.text, "html.parser")
        # print(html)
        self.data = html.body.find_all('div')[2].table.find_all('tr')[
            3].find_all('td')[3].table
        return True

    def to_html(self):
        return self.data

    def to_json(self):
        return json.dumps({'html': str(self.data)})

class CJ(Client):
    host = 'http://cj.shu.edu.cn'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def __init__(self, card_id, password):
        Client.__init__(self, card_id, password)

    def login(self):
        r = self.session.get(
            self.host + '/User/GetValidateCode?%20%20+%20GetTimestamp()', timeout=10, stream=True, proxies=get_proxies())
        self.captcha = captcha_solver.create(
            r.raw.read(), site='XK')['Result']
        post_data = {'url': '',
                     'txtUserNo': self.card_id,
                     'txtPassword': self.password,
                     'txtValidateCode': self.captcha}
        r = self.session.post(self.host + '/',
                        data=post_data, headers=self.headers, timeout=60, proxies=get_proxies())
        r = self.session.get(
            self.host + '/Home/StudentIndex', timeout=10, proxies=get_proxies())
        # if r.text.find(u'验证码错误') != -1 or r.text.find(u'帐号或密码错误')!=-1 or r.text.find(u'教学评估') != -1:
        # print(r.text)
        return r.text.find('首页') != -1

    def score_query(self,academic_term_id):
        # r = self.session.get(self.host+'/StudentPortal/ScoreQuery')
        r = self.session.post(self.host+'/StudentPortal/CtrlScoreQuery',data={'academicTermID':academic_term_id})
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.findAll('table')
        rows = table.findAll('tr')[2:]
        scores = []
        for row in rows:
            cells = row.findAll("td")
            score = {
                'courseNo':cells[1],
                'courseName':cells[2],
                'credit': cells[3],
                'grade': cells[4],
                'gradePoint':cells[5]
            }
            scores.append(score)
        return scores

    def get_score_summary():
        r = self.session.get(self.host+'/StudentPortal/ScoreSummary')
        soup = BeautifulSoup(r.text,"html.parser")
        content = soup.find('.div_master_content')
        return content

    def get_score_trend():
        r = self.session.get(self.host+'/StudentPortal/ScoreTrend')
        soup = BeautifulSoup(r.text,'html.parser')
        trend = soup.find('#ScoreTrend')
        return trend.value

    def get_data(self):
        r = self.session.get(
            self.host + '/StudentPortal/ScoreQuery', timeout=20, proxies=get_proxies())
        content = re.search(
            r'<table class="tbllist">([\s\S]*?)</table>', r.text, flags=0).group(0)
        self.data = content
        return True

    def to_html(self):
        return self.data


# class ComTest(Client):
#     host = 'http://ea.cc.shu.edu.cn/login'

#     def login(self):
#         self.s = requests.Session()
#         postData = {'username': self.card_id,
#                     'password': self.password}
#         r = self.s.post(self.host, data=postData,
#                         timeout=30, proxies=proxies,proxies=get_proxies())
#         if r.text != u'学号或密码错误':
#             self.is_login = True
#         return True

#     def get_data(self):
#         string = r.text
#         content = re.search(
#             r'<table class="table table-hover">([\s\S]*)</form>', string, flags=0).group(0)
#         content = re.sub(r'<table class="table table-hover">',
#                          '<table>', content)
#         self.data = content
#         return True

#     def to_json(self):
#         return {
#             'type': 'html',
#             'data': self.data
#         }

# class Lehu(Client):
#     host = 'http://card.lehu.shu.edu.cn'

#     def login(self):
#         post_data = {'username': self.card_id,
#                      'password': self.password,
#                      'url': 'http://www.lehu.shu.edu.cn/'}
#         r = self.session.post(
#             'http://passport.lehu.shu.edu.cn/ShowOrgUserInfo.aspx', data=post_data, timeout=30, proxies=get_proxies())
#         return r.text != u'1|password|一卡通账号不存在或密码错误！'

#     def get_data(self):
#         r = self.session.get(
#             self.host + '/CardTradeDetail.aspx', timeout=30)
#         content = re.search(
#             r'<span id="ctl00_Contentplaceholder1_Label1">([\s\S]*)</form>', r.text, flags=0).group(0)
#         self.data = content
#         return True

#     def to_html(self):
#         return self.data

#     def to_json(self):
#         return {
#             'html': self.data
#         }

