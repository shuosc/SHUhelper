'''
Find Empty Room
'''
import os
import json
import SHUhelper.schooltime
from SHUhelper import app
CLASSROOM_DICT = {}
JSON_FILE = open(os.path.join(app.root_path, 'classroomdata.json'))
CLASSROOM_DICT = json.load(JSON_FILE)

def is_room_empty(room, week, day, time):
    return CLASSROOM_DICT[room][week][day][time] == 1

def get_emptyroom_now():
    week = SHUhelper.schooltime.this_week()
    day = SHUhelper.schooltime.this_day()
    time = SHUhelper.schooltime.this_class()
    return get_emptyroom(week, day, time)

def get_emptyroom(week, day, time):
    emptyroom_list = []
    if time == 0 or day == 0 or day == 6:
        return emptyroom_list
    for classroom in CLASSROOM_DICT.keys():
        if CLASSROOM_DICT[classroom][week-1][day-1][time-1] == 1:
            emptyroom_list.append(classroom)
    return sorted(emptyroom_list)

