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

def general_login(site,user,pwd): #不使用验证码登录的网站的通用登录方法
    if site == 'pe':#根据相应网站确定相应的postData
        postData={'UNumber':user,'Upwd':pwd,'USnumber':u'上海大学'}
    elif site == 'finold':
        postData={'__EVENTTARGET':'',
    '__EVENTARGUMENT':'',
    '__VIEWSTATE':'/wEPDwUKLTM3NDg5MjY1NQ9kFgICAQ9kFgICAw9kFhACAQ8PFgIeBFRleHQFNw0KCQkJCQkJCQkJCTxiPueZu+W9leezu+e7nzwvYj7vvIjmnKznp5HmlLbotLnmn6Xor6LvvIlkZAIDDw8WAh4LTmF2aWdhdGVVcmwFNExvZ2luLmFzcHg/UmV0dXJuVXJsPSUyZlR1aXRpb24uYXNweCZFbXBsb3llZUxvZ2luPTFkZAITDw8WAh4HVmlzaWJsZWdkZAIUDw8WBB8ABcQBPGltZyBzcmM9cGljLzEuZ2lmIGJvcmRlcj0wPjxpbWcgc3JjPXBpYy8xLmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvNS5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzUuZ2lmIGJvcmRlcj0wPjxpbWcgc3JjPXBpYy84LmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvNy5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzQuZ2lmIGJvcmRlcj0wPh8CZ2RkAhYPDxYCHwJnZGQCFw8PFgQfAAWoATxpbWcgc3JjPXBpYy81LmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvNS5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzUuZ2lmIGJvcmRlcj0wPjxpbWcgc3JjPXBpYy83LmdpZiBib3JkZXI9MD48aW1nIHNyYz1waWMvMi5naWYgYm9yZGVyPTA+PGltZyBzcmM9cGljLzQuZ2lmIGJvcmRlcj0wPh8CZ2RkAhkPDxYCHwJnZGQCGw8PFgIfAmdkZGTkUiQcxLjI7qbIyEZc3bENY5Ztjw==',
    '__EVENTVALIDATION':'/wEWBAKXm79JAtXh0pgPAqW0mtsGApOzq+INgXLh/Sj8FgD/gUxZsNSw4Q5MHNc=',
    'login1$txtName':user,
    'login1$txtPsw':pwd,
    'login1$Button1':''}
    elif site == 'lehu':
        postData={'username':user,'password':pwd,'url':'http://www.lehu.shu.edu.cn/'}
    else:
        return False
    
    s = requests.session()#session初始化
    #根据不同site发出不同的网络请求
    try:
        if site == 'pe':
            r = s.get('http://202.120.127.149:8989/spims/login/index.jsp',timeout=10)
            r = s.post('http://202.120.127.149:8989/spims/login.do?method=toLogin',data=postData,timeout=10)
            r = s.get('http://202.120.127.149:8989/spims/exercise.do?method=seacheload',timeout=10)
            string = r.text
        elif site == 'finold':
            r = s.post('http://finance.shu.edu.cn/Login.aspx?ReturnUrl=%2fTuition.aspx',data=postData,timeout=30)
            string = r.text
        elif site == 'lehu':
            r = s.post('http://passport.lehu.shu.edu.cn/ShowOrgUserInfo.aspx',data=postData,timeout=30)
            r = s.get('http://card.lehu.shu.edu.cn/CardTradeDetail.aspx',timeout=30)
            string = r.text
    except:
        return False
    else:
        #根据不同site进行不同的文本处理
        if site == 'pe':
            content=re.search(r'<table cellpadding="3" cellspacing="1" class="table_bg">([\s\S]*)<tr>\s+<td colspan="13">',string,flags=0).group(0)
            content = re.sub(r'<table cellpadding="3" cellspacing="1" class="table_bg">','<table class="table table-hover">',content)
        elif site == 'finold':
            content = re.search(r'<table id="Table1" cellspacing="0" cellpadding="0" width="759" align="center" border="0">([\s\S]*)</table>',string,flags=0).group(0)
            content = re.sub(r'<span id="Tuition1_Label2">([\s\S]*)</select>', "", content)
            content = re.sub(r"<font color='red'>([\s\S]*?)</font>", "", content)
        elif site == 'lehu':
            content = re.search(r'<span id="ctl00_Contentplaceholder1_Label1">([\s\S]*)</form>',string,flags=0).group(0)
        return content
    return False

def finquest():
    from PIL import Image
    from io import BytesIO
    s = requests.Session()
    r = s.get('http://xssf.shu.edu.cn:8100/SFP_Share/Home/CheckImgCode',timeout=10)
    return BytesIO(r.content).getvalue().encode('base64') , s.cookies

def finlogin(cookies,user,pwd,check):
    postData={'userName':user,
    'pwd':pwd,
    'ktextbox':check,
    'hidCheckCode':''}
    s = requests.Session()
    try:
        r = s.post('http://xssf.shu.edu.cn:8100/SFP_Share/?Length=5',data=postData,timeout=10,cookies=cookies)
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_PersonInfo',timeout=10)
        personinfo = re.search(r'(<fieldset([\s\S]*)</fieldset>)',r.text,flags=0).group(0)
        r =s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryPaymentcondition',timeout=10)
        paymentcondition = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        arrearageAmount = re.search(r'[0-9]\d*.[0-9]\d*',r.text,flags=0).group(0)
        personinfo = re.sub(r'<span id="arrearageAmount"></span>',arrearageAmount,personinfo)
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryChargeRecord',timeout=10)
        chargerecord = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_ChargeSelf/StudentPaymentQuery/Ctrl_QueryRefundRecord',timeout=10)
        refundrecord = re.search(r'(<table([\s\S]*)</table>)',r.text,flags=0).group(0)
        string = personinfo+u'<legend></legend><legend>缴费情况</legend>'+paymentcondition+u'<legend>缴费记录</legend>'+chargerecord+u'<legend>退费记录</legend>'+refundrecord+u'<legend></legend>'
        string = re.sub(r'<table class="tblList tblInLine">','<table class="table table-hover">',string)
    except:
        return False
    else:
        return string

def phyquest():
    from PIL import Image
    from io import BytesIO
    s = requests.Session()
    r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/login/',timeout=10)
    phyhash = re.search(r'<input type="hidden" name="__hash__" value="([\s\S]*)" />',r.text,flags=0).group(1)
    r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/verify/',timeout=10)
    return BytesIO(r.content).getvalue().encode('base64') , s.cookies , phyhash

def phylogin(cookies,phyhash,user,pwd,check):
    postData={'_hash_':phyhash,
    'account':user,
    'ajax':'1',
    'password':pwd,
    'verify':check}
    s = requests.Session()
    try:
        r = s.post('http://www.phylab.shu.edu.cn/openexp/index.php/Public/checkLogin/',data=postData,timeout=10,cookies=cookies)
        r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/main',timeout=10,cookies=cookies)
        string = re.search(r'(<TABLE([\s\S]*?)</TABLE>)',r.text,flags=0).group(0)
        string = re.sub(r'<TABLE id="checkList" class="list" cellpadding=0 cellspacing=0 >','<table class="table table-hover" cellpadding="0" cellspacing="0" >',string)
        string = re.sub(r'<input type="submit" name="submit1"','<input type="submit" name="submit1" class="btn btn-large btn-info" ',string)
    except:
        return False
    else:
        return string
def nhce(user,pwd,cid):
    postData={'password':'nhce111','username':user}
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


@app.route('/nhce', methods=['POST', 'GET'])
def nhceroute():
    if request.method == 'POST':
        r = nhce(request.form['username'],request.form['password'],request.form['CID'])
        if(r!=False):
            resp = make_response(render_template('nhce.html', error=r , check=None))
        else:
            resp = make_response(render_template('nhce.html', error=u'注册失败！请重新尝试,请注意初始密码为 nhce111' , check=None))
    elif request.method == 'GET':
        resp = make_response(render_template('nhce.html', error=u'请注意初始密码为 nhce111' , check=None))
    return resp

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
@app.route('/tel')
def tel():
    resp = make_response(render_template('tel.html'))
    return resp

@app.route('/login/<check>/<site>', methods=['POST', 'GET'])
#check变量代表此接口是否有验证码
#site变量代表发生此接口是哪个接口
def login(site,check):
    error = None
    if check != 'vali':
        check = None
    if request.method == 'POST':
        if site == 'pe' or site =='finold' or site == 'lehu':
            r = general_login(site,request.form['username'],request.form['password'])
        elif site == 'phylab':
            usercookies = requests.cookies.RequestsCookieJar()
            usercookies.set('PHPSESSID',request.cookies.get('PHPSESSID'))
            r = phylogin(usercookies,request.cookies.get('_hash_'),request.form['username'],request.form['password'],request.form['check'])
        elif site == 'fin':
            usercookies = requests.cookies.RequestsCookieJar()
            usercookies.set('ASP.NET_SessionId',request.cookies.get('ASP.NET_SessionId'))
            usercookies.set('SFP_Verify_Cookie',request.cookies.get('SFP_Verify_Cookie'))
            r = finlogin(usercookies,request.form['username'],request.form['password'],request.form['check'])
        elif site == 'nhce':
            r = nhce(request.form['username'],request.form['password'],request.form['CID'])
        else:
            return render_template('index.html', error=error)
        if r != False:
            return render_template(site+'.html', r=r)
        else:
            error = u'登录失败！可能是账户密码错误或服务器宕机'
            return render_template('login.html', error=error , check=check)
    elif request.method == 'GET':
        if site == 'fin':
            r,cookies = finquest()
            error = u'请注意！若未修改过密码，初始密码为身份证后六位或学号后六位！！'
            resp = make_response(render_template('login.html',r=r , error=error , check=check))
            for cj in cookies:
                resp.set_cookie(cj.name,cj.value)
            return resp
        elif site == 'phylab':
            r,cookies,phyhash = phyquest()
            error = u'请注意！若未修改过密码，初始密码为学号！！'
            resp = make_response(render_template('login.html',r=r , error=error , check=check))
            for cj in cookies:
               resp.set_cookie(cj.name,cj.value)
            resp.set_cookie('_hash_',phyhash)
            return resp
        elif site =='nhce':
             resp = make_response(render_template('nhce.html',r=r , error=error , check=check))
        else:
            return render_template('login.html', error=error,check=check)
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

