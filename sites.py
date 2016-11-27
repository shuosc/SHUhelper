#! python3
#coding=utf-8
import re
import requests
import base64
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
    except:
        return False
    if success:
        return s
    else:
        return False
def getcontent(site, s):
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
        return content
    except:
        return False
def getCAPTCHA(site, s):
    from PIL import Image
    from io import BytesIO
    phyhash = None
    if site == 'fin':
        r = s.get('http://xssf.shu.edu.cn:8100/SFP_Share/Home/CheckImgCode',timeout=10,stream=True)
    elif site == 'phylab':
        r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/login/',timeout=10)
        phyhash = re.search(r'<input type="hidden" name="__hash__" value="([\s\S]*)" />',r.text,flags=0).group(1)
        r = s.get('http://www.phylab.shu.edu.cn/openexp/index.php/Public/verify/',timeout=10,stream=True)
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
def test():
    return 1

