#! python3
#coding=utf-8
import re
import requests
import base64
from bs4 import BeautifulSoup
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
    elif site == 'cj':
        postData={'url':'',
        'txtUserNo':user,
        'txtPassword':pwd,
        'txtValidateCode':check}
    elif site == 'xkc' or site =='xkl' :  # xkc for current semester, xkl for last semester
        postData = {'txtUserName':user,
        'txtPassword':pwd,
        'txtValiCode':check}
    else:
        return False
    try:
        if site == 'pe':
            r = s.get('http://202.120.127.149:8989/spims/login/index.jsp',timeout = 30)
            r = s.post('http://202.120.127.149:8989/spims/login.do?method=toLogin',data = postData, timeout = 30)
            success = r.headers['Content-Length'] == '784'
        elif site == 'lehu':
            r = s.post('http://passport.lehu.shu.edu.cn/ShowOrgUserInfo.aspx',data = postData,timeout = 30)
            success = r.text != u'1|password|一卡通账号不存在或密码错误！'
        elif site == 'phylab':
            r = s.post('http://www.phylab.shu.edu.cn/openexp/index.php/Public/checkLogin/',data = postData,timeout=10)
            success = r.text.find(u'false') != -1
        elif site == 'fin':
            r = s.post('http://xssf.shu.edu.cn:8100/SFP_Share/?Length=5',data = postData, timeout=10)
            r = s.get('http://xssf.shu.edu.cn:8100/SFP_Share/', timeout = 10)
            success = r.text.find(u'错误') == -1 and r.text.find(u'不正确') == -1
        elif site == 'cj':
            r = s.post('http://cj.shu.edu.cn/',data = postData,timeout=60)
            r = s.get('http://cj.shu.edu.cn/Home/StudentIndex',timeout=10)
            success = r.text.find(u'首页') != -1
        elif site == 'xkc':
            r = s.post('http://xk.shu.edu.cn/',data = postData,timeout=60)
            success = r.text.find(u'首页') != -1
        elif site == 'xkl':
            r = s.post('http://xk.shu.edu.cn:8080/',data = postData,timeout=60)
            success = r.text.find(u'首页') != -1
    except:
        return False
    if success:
        return s
    else:
        return False
        # return r.text
def get_content(site, s, option=''):
    try:
        if site == 'pe':
            r = s.get('http://202.120.127.149:8989/spims/exercise.do?method=seacheload',timeout=10)
            string = r.text
            content=re.search(r'<table cellpadding="3" cellspacing="1" class="table_bg">([\s\S]*)</table>' \
            , string,flags=0).group(0)
            content = re.sub(r'<table cellpadding="3" cellspacing="1" class="table_bg">' \
            , '<table class="table  table-striped table-hover table-bordered table-condensed">',content)

        elif site == 'lehu':
            r = s.get('http://card.lehu.shu.edu.cn/CardTradeDetail.aspx',timeout = 30)
            string = r.text
            content = re.search(r'<span id="ctl00_Contentplaceholder1_Label1">([\s\S]*)</form>',string,flags=0).group(0)
        elif site == 'phylab':
            r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/main',timeout=10)
            string = re.search(r'(<TABLE([\s\S]*?)</TABLE>)',r.text,flags=0).group(0)
            string = re.sub(r'<TABLE id="checkList" class="list" cellpadding=0 cellspacing=0 >' \
            , '<table class="table  table-striped table-hover table-bordered table-condensed" >',string)
            content = re.sub(r'<input type="submit" name="submit1"' \
            , '<input type="submit" name="submit1" class="btn btn-large btn-info" ',string)
        elif site == 'fin':
            r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_PersonInfo',timeout=10)
            personinfo = re.search(r'(<fieldset([\s\S]*)</fieldset>)',r.text,flags=0).group(0)
            r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryPaymentcondition',timeout=10)
            paymentcondition = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
            arrearageAmount = re.search(r'[0-9]\d*.[0-9]\d*',r.text,flags=0).group(0)
            personinfo = re.sub(r'<span id="arrearageAmount"></span>',arrearageAmount,personinfo)
            r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryChargeRecord',timeout=10)
            chargerecord = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
            r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryRefundRecord',timeout=10)
            refundrecord = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
            content = personinfo+u'<legend></legend><legend>缴费情况</legend>' \
            + paymentcondition+u'<legend>缴费记录</legend>'+chargerecord \
            + u'<legend>退费记录</legend>'+refundrecord+u'<legend></legend>'
            content = re.sub(r'<table class="tblList tblInLine">',\
            '<table class="table  table-striped table-hover table-bordered table-condensed">',content)
        elif site == 'cj':
            r = s.get('http://cj.shu.edu.cn/StudentPortal/ScoreQuery',timeout=20)
            string = re.search(r'<table class="tbllist">([\s\S]*?)</table>',r.text,flags=0).group(0)
            content = string
        elif site == 'xkc': # 使用([\s\S]*)以贪婪匹配
            r = s.get('http://xk.shu.edu.cn/StudentQuery/CtrlViewQueryCourseTable',timeout=20)
            string = re.search(r'<table class="tbllist">([\s\S]*)</table>',r.text,flags=0).group(0)
            content = string
        elif site == 'xkl':
            r = s.get('http://xk.shu.edu.cn:8080/StudentQuery/CtrlViewQueryCourseTable',timeout=20)
            string = re.search(r'<table class="tbllist">([\s\S]*)</table>',r.text,flags=0).group(0)
            content = string
        return content
    except:
        return False
def get_json_from_course_table(content):
    import json
    table =re.search(r'<table class="tbllist">([\s\S]*?)</table>',content,flags=0).group(0)
    soup = BeautifulSoup(table,"html.parser")
    table = soup.find("table")
    course_list = []
    for row in table.findAll("tr")[2:]:
        cells = row.findAll("td")[1:]
        data = {
        'courseno':cells[0].get_text(strip=True),
        'coursename':cells[1].get_text(strip=True),
        'teachno':cells[2].get_text(strip=True),
        'teachname':cells[3].get_text(strip=True),
        'credit':cells[4].get_text(strip=True),
        'coursetime':cells[5].get_text(strip=True),
        'courseplace':cells[6].get_text(strip=True),
        'campus':cells[7].get_text(strip=True),
        'qtime':cells[8].get_text(strip=True),
        'qplace':cells[9].get_text(strip=True)
        }
        course_list.append(data)
    return json.dumps(course_list)
def get_binary_json_from_course_table(content,week):
    import json
    cn_num={
        u'一':1,
        u'二':2,
        u'三':3,
        u'四':4,
        u'五':5,
    }
    time_table=[[],[],[],[],[]]
    data={
    'isempty':True,
    'coursename':coursename
    }
    for days in time_table:
        for i in range(1,14):
            days.append(data)
    table =re.search(r'<table class="tbllist">([\s\S]*?)</table>',content,flags=0).group(0)
    soup = BeautifulSoup(table,"html.parser")
    table = soup.find("table")
    for row in table.findAll("tr")[2:]:
        cells = row.findAll("td")[1:]
        coursename=cells[1].get_text(strip=True)
        coursetime=cells[5].get_text(strip=True)
        while(True):
            data={
            'isempty':True,
            'coursename':coursename
            }
            time = re.search(r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*',coursetime,flags=0)
            coursetime = re.sub(r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*','',coursetime,1)
            if time == None:
                break
            day = cn_num[time.group(1)]
            start = int(time.group(2))
            end = int(time.group(3))
            if time.group(4)!=None:
                if time.group(4) == u'单':
                    if week%2==1:
                        data['isempty']=False
                else:
                    if week%2==0:
                        data['isempty']=False
            elif time.group(5)!=None:
                if week<=int(time.group(5)) and week>=int(time.group(4)):
                    data['isempty']=False
            elif time.group(7)!=None:
                if week==int(time.group(7)) or week==int(time.group(8)):
                    data['isempty']=False
            for i in range(start,end):
                time_table[day][i] = data
    return json.dumps(time_table) 

# def detect_conflict(data):
#     time_list_raw = list_init()
#     for time_list in data:
#         for col in time_list:
#             for blocks in col:
#                 if blocks['isempty']==False:
#                     time_list_raw[]

def list_init():
    list_raw = [[],[],[],[],[]]
    data={
    'isempty':True,
    'coursename':coursename
    }
    for days in list_raw:
        for i in range(1,14):
            days.append(data)
    return list_raw
def get_CAPTCHA(site, s):
    from PIL import Image
    from io import BytesIO
    phyhash = None
    if site == 'fin':
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_Share/Home/CheckImgCode',timeout=10,stream=True)
    elif site == 'phylab':
        r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/login/',timeout=10)
        phyhash = re.search(r'<input type="hidden" name="__hash__" value="([\s\S]*)" />',r.text,flags=0).group(1)
        r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/verify/',timeout=10,stream=True)
    elif site == 'cj':
        r = s.get('http://cj.shu.edu.cn/',timeout=20)
        r = s.get('http://cj.shu.edu.cn/User/GetValidateCode?%20%20+%20GetTimestamp()',timeout=20,stream=True)
    elif site == 'xkc':
        r = s.get('http://xk.shu.edu.cn/',timeout=20)
        r = s.get('http://xk.shu.edu.cn/Login/GetValidateCode?%20%20+%20GetTimestamp()',timeout=20,stream=True)
    elif site == 'xkl':
        r = s.get('http://xk.shu.edu.cn:8080',timeout=20)
        r = s.get('http://xk.shu.edu.cn:8080/Login/GetValidateCode?%20%20+%20GetTimestamp()',timeout=20,stream=True)

    return base64.b64encode(r.raw.read()).decode('utf-8'), s, phyhash
def nhce(user,pwd,cid):
    # nhce111
    postData={'password':pwd,'username':user}
    postData2={'CID':cid,'Submit':'Confirm'}#Confirm
    s = requests.Session()
    try:
        r = s.get('http://nhce.shu.edu.cn')
        r = s.post('http://nhce.shu.edu.cn/index.php',data=postData,timeout=10)
        r = s.post('http://nhce.shu.edu.cn/login/classregister.php',data=postData2,timeout=10)
    except:
        return False
    else:
        if(re.search('Please login from the homepage',r.text.encode('utf-8'),flags=0) == None):
            return u'提交成功！请登录<a href="http://nhce.shu.edu.cn">nhce.shu.edu.cn</a>查看班级注册结果，如果不小心选错了可以在“班级注册”处注销班级重新选择'
        else:
            return False