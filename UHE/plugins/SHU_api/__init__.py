import requests
from bs4 import BeautifulSoup
from flask import Blueprint, jsonify, request

from UHE.plugins import UHEPlugin
from .client import Services

SHUapi = Blueprint('shu', __name__)
__plugin__ = "SHUAPI"

class SHU():
    def auth(user_id,password):
        pass

class Student():
    pass

class Teacher():
    pass

class SHUAPI(UHEPlugin):
    settings_key = 'SHU_api'

    def setup(self, app):
        app.register_blueprint(SHUapi, url_prefix='/shu')
        # app.university = SHU()
        # app.student = Student

        print('setup', __plugin__)

    def install(self, app):
        pass

    def uninstall(self):
        print('uninstall')


def get_courses():
    pass


def auth_user(username, password):
    pass


@SHUapi.route('/info/')
def get_shu_info_single():
    category = request.args['category']
    msg_id = request.args['msgID']
    url = 'http://www.shu.edu.cn/info/{}/{}.htm'.format(category, msg_id)
    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.text, "html.parser")
    contents = soup.find(id="vsb_content").table.tr.td.contents
    return jsonify(content=str(contents[2]))

@SHUapi.route('/news/')
def get_news_api():
    pass


@SHUapi.route('/courses/')
def get_courses_api():

    pass
    return 'ok'


@SHUapi.route('/auth/')
def auth_user_api():
    pass
