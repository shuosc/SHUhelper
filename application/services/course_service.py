import datetime

from application.admin.views import BasicPrivateModelView
from application.calendar.models import Activity, Event
from application.extensions import admin
from .courses import courses
from .teachers import teachers
from .evaluations import evaluations
from .manage import get_xk
from .models import Course, CourseOfTerm, Teacher, Evaluation

# from celery.contrib.methods import task_method
__plugin__ = "SHUCourse"

date = datetime.datetime
delta = datetime.timedelta

class CourseOfTermView(BasicPrivateModelView):
    column_filters = ['course_no', 'teacher_name', 'term']
    column_searchable_list = ('course_no', 'teacher_name')


class TeacherView(BasicPrivateModelView):
    column_searchable_list = ('name', 'no')

class CourseView(BasicPrivateModelView):
    # can_delete = False
    form_ajax_refs = {
        'teacher': {
            'fields': ['no']
        }
    }
    column_searchable_list = ('no', 'teacher_name')
    # can_create = False
    can_export = True


class SHUCourse(applicationPlugin):
    settings_key = 'SHU_course'

    def setup(self, app):
        admin.add_view(
            CourseOfTermView(CourseOfTerm, endpoint='course-term-manage'))
        admin.add_view(
            BasicPrivateModelView(Evaluation, endpoint='evaluations-manage'))
        admin.add_view(CourseView(Course, endpoint='course-manage'))
        admin.add_view(TeacherView(Teacher, endpoint='teacher-manage'))
        app.register_blueprint(courses, url_prefix='/courses')
        app.register_blueprint(teachers, url_prefix='/teachers')
        app.register_blueprint(evaluations, url_prefix='/evaluations')
        print('setup', __plugin__)

    def install(self, app):
        get_xk('http://xk.shu.edu.cn:8080/')
        get_xk('http://xk.shu.edu.cn/')

    def uninstall(self):
        print('uninstall')
        event = Event.objects(
            identifier="SHU_calendar_%s" % year).first()
        Activity.objects(event=event).delete()
        event.delete()
