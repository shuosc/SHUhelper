from UHE.calendar.models import Activity, Event
from UHE.plugins import UHEPlugin
from UHE.plugins.SHU_course.models import CourseOfTerm
# from celery.contrib.methods import task_method
__plugin__ = "SHUCourseToCalendar"


class SHUCourseToCalendar(UHEPlugin):
    settings_key = 'SHU_course_to_calendar'

    def setup(self,app):
        print('setup', __plugin__)

    def install(self, app):
        courses = CourseOfTerm.objects(term='2017_1')

        for course in courses:
            pass
    def uninstall(self):
        print('uninstall')
        event = Event.objects(
            identifier="SHU_calendar_%s" % year).first()
        Activity.objects(event=event).delete()
        event.delete()
