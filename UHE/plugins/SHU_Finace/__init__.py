import datetime
import json

from bs4 import BeautifulSoup
from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_required

from UHE.client import Client
from UHE.plugins import UHEPlugin
from UHE.user.models import UserData

# from celery.contrib.methods import task_method
__plugin__ = "SHUFin"


fin = Blueprint('fin', __name__)


class Fin(Client):
    url_prefix = 'http://xssf.shu.edu.cn:8100'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def login(self):
        # r = self.session.get(
        #     'http://xssf.shu.edu.cn:8088/LocalLogin.aspx',timeout=10)
        # soup = eautifulSoup(r.text, "html.parser")
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


@fin.route('/sync', methods=['GET', 'POST'])
@login_required
def index_sync():
    if request.method == 'GET':
        data = UserData.objects(user=current_user.id,
                                identifier=__plugin__).get_or_404()
        return jsonify(data)
    else:
        post_data = request.get_json()
        user_data = UserData.objects(
            user=current_user.id, identifier=__plugin__).first()
        if user_data is None:
            user_data = UserData(identifier=__plugin__,
                                 user=current_user.id, status='none')
            user_data.save()
        task = get_data(post_data['card_id'], post_data['password'])
        return jsonify(success='ok')


def get_data(card_id, password):
    user_data = UserData.objects(user=card_id, identifier=__plugin__).first()
    user_data.status = 'pending'
    user_data.save()
    try:
        client = Fin(card_id, password)
        client.login()
        client.get_data()
    except Exception as e:
        user_data.status = 'failed'
        user_data.save()
        print('error')
        raise e
    user_data.data = client.to_json()
    user_data.status = 'success'
    user_data.last_modified = datetime.datetime.now()
    user_data.lock_save(password)


@fin.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        data = UserData.objects(user=current_user.id,
                                identifier=__plugin__).get_or_404()
        return jsonify(data)
    else:
        post_data = request.get_json()
        user_data = UserData.objects(
            user=current_user.id, identifier=__plugin__).first()
        if user_data is None:
            user_data = UserData(identifier=__plugin__,
                                 user=current_user.id, status='none')
            user_data.save()
        task = get_data.delay(post_data['card_id'], post_data['password'])
        return jsonify(success=task.id)

@fin.route('/status')
@login_required
def status():
    data = UserData.objects(user=current_user.id,
                                identifier=__plugin__).get_or_404()
    return jsonify(data.status)

# @my_course.route('/sync', methods=['GET', 'POST'])
# def sync_index():
#     if request.method == 'GET':
#         data = UserData.objects(user=current_user.id,
#                                 identifier=__plugin__).get_or_404()
#         return jsonify(data)
#     else:
#         post_data = request.get_json()
#         user_data = UserData.objects(
#             user=current_user.id, identifier=__plugin__).first()
#         if user_data is None:
#             user_data = UserData(identifier=__plugin__,
#                                  user=current_user.id, status='none')
#             user_data.save()
#         task = get_course(post_data['card_id'], post_data['password'])
#         return jsonify(success='ok')


# @celery.task
# def get_course(card_id, password):
#     user_data = UserData.objects(user=card_id, identifier=__plugin__).first()
#     user_data.status = 'pending'
#     user_data.save()
#     try:
#         client = XK(card_id, password)
#         client.captcha = captcha_solver.create(
#             client.captcha_img, site='XK')['Result']
#         print(client.captcha)
#         client.login()
#         client.get_data()
#     except Exception as e:
#         user_data.status = 'failed'
#         user_data.save()
#         print('error')
#         raise e
#         return
#     user_data.data = client.to_json()
#     user_data.status = 'success'
#     user_data.last_modified = datetime.datetime.now()
#     user_data.save()


class SHUFin(UHEPlugin):
    settings_key = 'SHU_calendar'

    def setup(self, app):
        # self.app = current_app
        # print(current_app)
        current_app.register_blueprint(fin, url_prefix='/fin')

        print('setup', __plugin__)
        # print(current_app.url_map)

    def install(self, app):
        pass

    def uninstall(self):
        print('uninstall')
        pass
