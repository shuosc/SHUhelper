
import re

from flask import Blueprint, current_app, jsonify, request
from UHE.calendar.models import Activity, Event
from UHE.extensions import redis_store
from .empty_room import EmptyRoom
from blinker import signal

app_start = signal('app_start')
empty_room = Blueprint('empty_room', __name__)

# find_empty_room = None


@app_start.connect
def init_rooms(app):
    classroom_dict = redis_store.get(
        'empty_room:' + app.school_time.term_string)
    app.find_empty_room = EmptyRoom(classroom_dict)


@empty_room.route('/')
def findemptyroom():
    campus = request.args.get('campus')
    week = request.args.get('week')
    day = request.args.get('day')
    course = request.args.get('course')
    if not week or not day or not course:
        time = current_app.school_time.time
        result = {
            'time': {'campus': '本部',
                     'year': time.year,
                     'term': time.term,
                     'week': time.week,
                     'day': time.day,
                     'course': time.course
                     },
            'rooms': current_app.find_empty_room.get_emptyroom('本部', int(time.week), int(time.day), int(time.course))
        }
    else:
        result = {
            'time': {
                'week': week,
                'day': day,
                'course': course,
                'campus': campus
            },
            'rooms': current_app.find_empty_room.get_emptyroom(campus, int(week), int(day), int(course))
        }
    return jsonify(result)


# @empty_room.route('/<room>')
# def room_schedule(room):
#     result = {
#         'room': room,
#         'schedule': find_empty_room.get_room_schedule(room)
#     }
#     return jsonify(result)
