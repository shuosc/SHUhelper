from flask import Blueprint
from UHE.calendar.models import Activity, Event
from UHE.plugins import UHEPlugin
from UHE.plugins.SHU_course.models import CourseOfTerm
from flask import Blueprint,request

from UHE.calendar.models import Activity, Event
from UHE.plugins import UHEPlugin
from UHE.plugins.SHU_course.models import CourseOfTerm

# from celery.contrib.methods import task_method
__plugin__ = "SHUEmptyRoom"

empty_room = Blueprint('empty_room', __name__)
@empty_room.route('/classrooms/empty')
def findemptyroom():
    week = request.args.get('week')
    day = request.args.get('day')
    time = request.args.get('time')
    if not week or not day or not time:
        result = {
            'week': schooltime.this_week(),
            'day': schooltime.this_day(),
            'time': schooltime.this_class(),
            'rooms': empty_room.get_emptyroom_now()
        }
    else:
        result = {
            'week': week,
            'day': day,
            'time': time,
            'rooms': empty_room.get_emptyroom(int(week), int(day), int(time))
        }
    return jsonify(result)

@empty_room.route('/classrooms/<room>')
def room_schedule(room):
    result = {
        'room': room,
        'schedule': empty_room.get_room_schedule(room)
    }
    return jsonify(result)


class SHUEmptyRoom(UHEPlugin):
    settings_key = 'SHU_calendar'

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
