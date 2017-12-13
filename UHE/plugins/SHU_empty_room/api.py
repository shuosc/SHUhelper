
import re

from flask import Blueprint, current_app, jsonify, request
from UHE.calendar.models import Activity, Event
from UHE.extensions import redis_store
from UHE.time import Time
from .empty_room import EmptyRoom

empty_room = Blueprint('empty_room', __name__)


@empty_room.route('/')
def findemptyroom():
    this_term = Time().term_string()
    classroom_dict = redis_store.get('empty_room_' + this_term)
    assert classroom_dict is not None
    find_empty_room = EmptyRoom(classroom_dict) 
    campus = request.args.get('campus')
    week = request.args.get('week')
    day = request.args.get('day')
    course = request.args.get('course')
    if not week or not day or not course:
        time_tuple = Time().time_tuple()
        result = {
            'campus': '本部',
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
            'rooms': find_empty_room.get_emptyroom(campus, int(week), int(day), int(course))
        }
    return jsonify(result)


# @empty_room.route('/<room>')
# def room_schedule(room):
#     result = {
#         'room': room,
#         'schedule': find_empty_room.get_room_schedule(room)
#     }
#     return jsonify(result)
