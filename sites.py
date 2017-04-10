import base64
import random
import re
import time

import requests
from bs4 import BeautifulSoup

from SHUhelper.models import CourseTest, db

proxies = {
  "http": "http://115.159.215.83:3128/",
  "https": "http://115.159.215.83:3128/",
}

# proxies = None

def general_login(s, site, user, pwd, check = None, other = None): #网站的通用登录方法
    if site == 'pe':#根据相应网站确定相应的postData
        postData={'UNumber':user,
        'Upwd':pwd,
        'USnumber':u'上海大学'}
    elif site == 'lehu':
        postData={'username':user,
        'password':pwd,
        'url':'http://www.lehu.shu.edu.cn/'}
    elif site == 'phylab':
        postData={'_hash_':other,
        'account':user,
        'ajax':'1',
        'password':pwd,
        'verify':check}
    elif site == 'fin':
        postData={'userName':user,
        'pwd':pwd,
        'ktextbox':check,
        'hidCheckCode':''}
    elif site == 'cjg' or site == 'cjt':
        postData={'url':'',
        'txtUserNo':user,
        'txtPassword':pwd,
        'txtValidateCode':check}
    elif site == 'xkc' or site =='xkl' :  # xkc for current semester, xkl for last semester
        postData = {'txtUserName':user,
        'txtPassword':pwd,
        'txtValiCode':check}
    elif site == 'quit':
        postData = {
            'ScriptManager1':'UpdatePanel1|bt_login',
            '__EVENTTARGET':'',
            '__EVENTARGUMENT':'',
            'tb_user':user,
            'tb_pass':pwd,
            'yzm':check,
            '__VIEWSTATE':'/wEPDwUKLTIyNjMwOTQ0OA9kFgICAw9kFgICAw9kFgJmD2QWAgIGDw8WAh4ISW1hZ2VVcmwFC0dldFBpYy5hc3B4ZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFCGJ0X2xvZ2lucNyfiFRRXGtQdyCrsDR27ZocM2JnEdaMAipvieykqB0=',
            '__ASYNCPOST':'true',
            'bt_login.x':'36',
            'bt_login.y':'25'
        }
    else:
        return False
    try:
        success = 'error'
        if site == 'pe':
            r = s.get('http://202.120.127.149:8989/spims/login/index.jsp',timeout = 30,proxies=proxies)
            r = s.post('http://202.120.127.149:8989/spims/login.do?method=toLogin',data = postData, timeout = 30,proxies=proxies)
            if(r.headers['Content-Length'] == '784'):
                success = 'success'
        elif site == 'lehu':
            r = s.post('http://passport.lehu.shu.edu.cn/ShowOrgUserInfo.aspx',data = postData,timeout = 30,proxies=proxies)
            if r.text != u'1|password|一卡通账号不存在或密码错误！':
                success = 'success'
        elif site == 'phylab':
            r = s.post('http://www.phylab.shu.edu.cn/openexp/index.php/Public/checkLogin/',data = postData,timeout=10,proxies=proxies)
            if r.text.find(u'false') != -1 :
                 success = 'success'
        elif site == 'fin':
            r = s.post('http://xssf.shu.edu.cn:8100/SFP_Share/?Length=5',data = postData, timeout=10,proxies=proxies)
            r = s.get('http://xssf.shu.edu.cn:8100/SFP_Share/', timeout = 10,proxies=proxies)
            if r.text.find(u'错误') == -1 and r.text.find(u'不正确') == -1:
                success = 'success'
        elif site == 'cjg' or site == 'cjt':#成绩查询
            r = s.post('http://cj.shu.edu.cn/',data = postData,timeout=60,proxies=proxies)
            r = s.get('http://cj.shu.edu.cn/Home/StudentIndex',timeout=10,proxies=proxies)
            if r.text.find(u'首页') != -1:
                success = 'success'
        elif site == 'xkc':
            r = s.post('http://xk.autoisp.shu.edu.cn:8080/',data = postData,timeout=60,proxies=proxies)
            if r.text.find(u'验证码错误') != -1:
                success = 'error_vali'
            elif r.text.find(u'帐号或密码错误')!=-1:
                success = 'error_pwd'
            elif r.text.find(u'教学评估') != -1:
                success = 'error_cj'
            elif r.text.find(u'首页') != -1:
                success = 'success'
            else:
                success = 'error'
        elif site == 'xkl':
            r = s.post('http://xk.autoisp.shu.edu.cn/',data = postData,timeout=60,proxies=proxies)
            if r.text.find(u'验证码错误') != -1:
                success = 'error_vali'
            elif r.text.find(u'帐号或密码错误')!=-1:
                success = 'error_pwd'
            elif r.text.find(u'教学评估') != -1:
                success = 'error_cj'
            elif r.text.find(u'首页') != -1:
                success = 'success'
            else:
                success = 'error'
        elif site == 'quit':
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
                'Referer':'http://www.act.shu.edu.cn/Login.aspx',
                'X-Requested-With':'XMLHttpRequest',
                'X-MicrosoftAjax': 'Delta=true',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
            }
            r = s.post('http://www.act.shu.edu.cn/Login.aspx', data=postData, timeout=30,proxies=proxies,headers=headers)
            if r.text.find('pageRedirect') != -1:
                success = 'success'
            else:
                success = 'error'
    except:
        return 'error',s
    return success , s
def get_content(site, s, option=''):
    if site == 'cjt':
        r = s.post('http://cj.shu.edu.cn/StudentPortal/CtrlStudentEnroll',data = {'academicTermID':'20162'},timeout=10,proxies=proxies)
        soup = BeautifulSoup( r.text,"html.parser")
        table = soup.find("table")
        row = table.findAll("tr")
        courselist = []
        for row in table.findAll("tr")[2:]:
            cells = row.findAll("td")
            course = {
                'courseno' : cells[0].get_text(strip=True),
                'coursename' : cells[1].get_text(strip=True),
                'teachno' : cells[2].get_text(strip=True),
                'teachename' : cells[3].get_text(strip=True),
                'date' : cells[4].get_text(strip=True),
                'time' : cells[5].get_text(strip=True),
                'place' : cells[6].get_text(strip=True),
                'delay' : cells[7].get_text(strip=True),
                'note' : cells[8].get_text(strip=True)
            }
            courselist.append(course)
            item = CourseTest.query.filter_by(courseno=course['courseno']).filter_by(teachno=course['teachno']).first()
            if item is None:
                item = CourseTest(courseno=course['courseno'],
                            coursename=course['coursename'],
                            teachno=course['teachno'],
                            teachename=course['teachename'],
                            date=course['date'],
                            time=course['time'],
                            place=course['place'],
                            delay=course['delay'],
                            note=course['note']
                            )
                db.session.add(item)
        db.session.commit()
        content = courselist
        return content
    if site == 'pe':
        r = s.get('http://202.120.127.149:8989/spims/exercise.do?method=seacheload',timeout=10,proxies=proxies)
        string = r.text
        content=re.search(r'<table cellpadding="3" cellspacing="1" class="table_bg">([\s\S]*)</table>' \
        , string,flags=0).group(0)
        content = re.sub(r'<table cellpadding="3" cellspacing="1" class="table_bg">' \
        , '<table class="table  table-striped table-hover table-bordered table-condensed">',content)

    elif site == 'lehu':
        r = s.get('http://card.lehu.shu.edu.cn/CardTradeDetail.aspx',timeout = 30,proxies=proxies)
        string = r.text
        content = re.search(r'<span id="ctl00_Contentplaceholder1_Label1">([\s\S]*)</form>',string,flags=0).group(0)
    elif site == 'phylab':
        r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/main',timeout=10,proxies=proxies)
        string = re.search(r'(<TABLE([\s\S]*?)</TABLE>)',r.text,flags=0).group(0)
        string = re.sub(r'<TABLE id="checkList" class="list" cellpadding=0 cellspacing=0 >' \
        , '<table class="table  table-striped table-hover table-bordered table-condensed" >',string)
        content = re.sub(r'<input type="submit" name="submit1"' \
        , '<input type="submit" name="submit1" class="btn btn-large btn-info" ',string)
    elif site == 'fin':
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_PersonInfo',timeout=10,proxies=proxies)
        personinfo = re.search(r'(<fieldset([\s\S]*)</fieldset>)',r.text,flags=0).group(0)
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryPaymentcondition',timeout=10,proxies=proxies)
        paymentcondition = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        arrearageAmount = re.search(r'[0-9]\d*.[0-9]\d*',r.text,flags=0).group(0)
        personinfo = re.sub(r'<span id="arrearageAmount"></span>',arrearageAmount,personinfo)
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryChargeRecord',timeout=10,proxies=proxies)
        chargerecord = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryRefundRecord',timeout=10,proxies=proxies)
        refundrecord = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        content = personinfo+u'<legend></legend><legend>缴费情况</legend>' \
        + paymentcondition+u'<legend>缴费记录</legend>'+chargerecord \
        + u'<legend>退费记录</legend>'+refundrecord+u'<legend></legend>'
        content = re.sub(r'<table class="tblList tblInLine">',\
        '<table class="table  table-striped table-hover table-bordered table-condensed">',content)
    elif site == 'cjg':
        r = s.get('http://cj.shu.edu.cn/StudentPortal/ScoreQuery',timeout=20,proxies=proxies)
        string = re.search(r'<table class="tbllist">([\s\S]*?)</table>',r.text,flags=0).group(0)
        content = string
    elif site == 'xkc': # 使用([\s\S]*)以贪婪匹配
        time.sleep(2)
        r = s.get('http://xk.autoisp.shu.edu.cn:8080/StudentQuery/CtrlViewQueryCourseTable',timeout=20,proxies=proxies)
        s.get('http://xk.autoisp.shu.edu.cn:8080/Login/Logout',proxies=proxies)
        string = re.search(r'<table class="tbllist">([\s\S]*?)</table>',r.text,flags=0).group(0)
        content = string
        # except:
        #     return r.text
    elif site == 'xkl':
        time.sleep(2)
        r = s.get('http://xk.autoisp.shu.edu.cn/StudentQuery/CtrlViewQueryCourseTable',timeout=20,proxies=proxies)
        string = re.search(r'<table class="tbllist">([\s\S]*?)</table>',r.text,flags=0).group(0)
        content = string
    elif site == 'quit':
        r = s.get('http://www.act.shu.edu.cn/Student/StudentMain.aspx',timeout=20,proxies=proxies)
        # print(r.text)
        r = s.get('http://www.act.shu.edu.cn/Student/UserCenter.aspx',timeout=20,proxies=proxies)
        # print(r.text)
        name = re.search(r'<span id="lb_username"><b><font size="4">([\s\S]*?)</font></b></span>',r.text,flags=0).group(1)
        print(name)
        school = re.search(r'<span id="lb_xy"><font color="Olive">([\s\S]*?)</font></span>',r.text,flags=0).group(1)
        major = re.search(r'<span id="lb_zy"><font color="Olive">([\s\S]*?)</font></span>',r.text,flags=0).group(1)
        r = s.get('http://www.act.shu.edu.cn/PersInfo/StudentPhoto.aspx',timeout=20,stream=True,proxies=proxies)
        pic = base64.b64encode(r.raw.read()).decode('utf-8')
        content = {
            'name':name,
            'school':school,
            'major':major,
            'pic':pic
        }
    return content

def get_CAPTCHA(site,s):
    from io import BytesIO
    phyhash = None
    if site == 'fin':
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_Share/Home/CheckImgCode',timeout=10,stream=True,proxies=proxies)
    elif site == 'phylab':
        r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/login/',timeout=10,proxies=proxies)
        phyhash = re.search(r'<input type="hidden" name="__hash__" value="([\s\S]*)" />',r.text,flags=0).group(1)
        r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/verify/',timeout=10,stream=True,proxies=proxies)
    elif site == 'cjt' or site =='cjg':
        r = s.get('http://cj.shu.edu.cn/',timeout=20,proxies=proxies)
        r = s.get('http://cj.shu.edu.cn/User/GetValidateCode?%20%20+%20GetTimestamp()',timeout=20,stream=True,proxies=proxies)
    elif site == 'xkc':
        r = s.get('http://xk.autoisp.shu.edu.cn:8080/Login/GetValidateCode?GetTimestamp()',timeout=20,stream=True,proxies=proxies)
        # time.sleep(5)
    elif site == 'xkl':
        r = s.get('http://xk.autoisp.shu.edu.cn/Login/GetValidateCode?GetTimestamp()',timeout=20,stream=True,proxies=proxies)
    elif site == 'quit':
        r = s.get('http://www.act.shu.edu.cn/Login.aspx',timeout=10,proxies=proxies)
        phyhash = re.search(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([\s\S]*)" />',r.text,flags=0).group(1)
        r = s.get('http://www.act.shu.edu.cn/GetPic.aspx',timeout=20,stream=True,proxies=proxies)
    return base64.b64encode(r.raw.read()).decode('utf-8'), s, phyhash
def nhce(user,pwd,cid):
    # nhce111
    postData={'password':pwd,'username':user}
    postData2={'CID':cid,'Submit':'Confirm'}#Confirm
    s = requests.Session()
    try:
        r = s.get('http://nhce.shu.edu.cn',proxies=proxies)
        r = s.post('http://nhce.shu.edu.cn/index.php',data=postData,timeout=10,proxies=proxies)
        r = s.post('http://nhce.shu.edu.cn/login/classregister.php',data=postData2,timeout=10,proxies=proxies)
    except:
        return False
    else:
        if(re.search('Please login from the homepage',r.text.encode('utf-8'),flags=0) == None):
            return u'提交成功！请登录<a href="http://nhce.shu.edu.cn">nhce.shu.edu.cn</a>查看班级注册结果，如果不小心选错了可以在“班级注册”处注销班级重新选择'
        else:
            return False
