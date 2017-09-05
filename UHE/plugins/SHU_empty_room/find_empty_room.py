"""
Find Empty Room
"""
import json
import os
import time
from UHE.utils import this_course, this_term, this_week, this_year
import os.path as op
# from flask import current_app
path = op.join(op.dirname(__file__), 'classroomdata.json')
JSON_FILE = open(path)
CLASSROOM_DICT = json.load(JSON_FILE)


def get_room_schedule(room):
    """
    return a schedule of a given room in this semster
    """
    return CLASSROOM_DICT.get(room)


def is_room_empty(room, week, day, course):
    """
    confirm weather the room is empty at the time
    """
    return CLASSROOM_DICT[room][week - 1][day - 1][course - 1] == 1


def get_emptyroom_now():
    """
    uses present time to get a list contain all free rooms
    """
    week = this_week()
    day = int(time.strftime("%w"))
    course = this_course()
    return get_emptyroom(week, day, course)


def get_emptyroom(week, day, course):
    """
    use custom time to get a list contain all free rooms
    """
    emptyroom_list = []
    if course == 0 or day == 0 or day == 6:
        return emptyroom_list
    for classroom in CLASSROOM_DICT.keys():
        if CLASSROOM_DICT[classroom][week - 1][day - 1][course - 1] == 1:
            emptyroom_list.append(classroom)
    return sorted(emptyroom_list)
