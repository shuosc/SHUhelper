import datetime
from flask import Blueprint
from UHE.calendar.models import Activity, Event
from UHE.plugins import UHEPlugin
from UHE.extensions import celery, captcha_solver, admin, db, plugin_manager
from flask_admin.contrib.mongoengine import ModelView
from mongoengine.context_managers import switch_collection
from bs4 import BeautifulSoup
from UHE.client import XK
import requests
import re
import time
# from celery.contrib.methods import task_method
__plugin__ = "SHUMyCourse"


my_course = Blueprint('my_course', __name__)


@my_course.route('/')
def index():

    pass

class SHUMyCourse(UHEPlugin):
    settings_key = 'SHU_calendar'

    def setup(self):
        self.app = plugin_manager.app
        self.app.register_blueprint(my_course, url_prefix='/my-course')

        print('setup', __plugin__)

    def install(self, app):
        get_xk('http://xk.shu.edu.cn:8080/')
        get_xk('http://xk.shu.edu.cn/')

    def uninstall(self):
        print('uninstall')
        event = Event.objects(
            identifier="SHU_calendar_%s" % (year)).first()
        Activity.objects(event=event).delete()
        event.delete()
