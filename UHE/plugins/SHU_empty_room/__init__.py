from flask import Blueprint, jsonify
from UHE.calendar.models import Activity, Event
from UHE.plugins import UHEPlugin
from UHE.plugins.SHU_course.models import CourseOfTerm
from flask import Blueprint, request, current_app

from UHE.calendar.models import Activity, Event
from UHE.plugins import UHEPlugin
from UHE.plugins.SHU_course.models import CourseOfTerm
from UHE.time import Time
from . import find_empty_room
# from celery.contrib.methods import task_method
__plugin__ = "SHUEmptyRoom"

empty_room = Blueprint('empty_room', __name__)


@empty_room.route('/')
def findemptyroom():
    week = request.args.get('week')
    day = request.args.get('day')
    course = request.args.get('course')
    if not week or not day or not course:
        time_tuple = Time().time_tuple()
        result = {
            'week': time_tuple[2],
            'day': time_tuple[3],
            'course': time_tuple[4],
            'rooms': find_empty_room.get_emptyroom_now()
        }
    else:
        result = {
            'week': week,
            'day': day,
            'course': course,
            'rooms': find_empty_room.get_emptyroom(int(week), int(day), int(course))
        }
    return jsonify(result)


@empty_room.route('/<room>')
def room_schedule(room):
    result = {
        'room': room,
        'schedule': find_empty_room.get_room_schedule(room)
    }
    return jsonify(result)


class SHUEmptyRoom(UHEPlugin):
    settings_key = 'SHU_calendar'

    def setup(self, app):
        print('setup', __plugin__)
        current_app.register_blueprint(empty_room, url_prefix='/empty-room')

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
