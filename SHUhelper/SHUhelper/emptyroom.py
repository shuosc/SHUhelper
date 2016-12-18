import json
import SHUhelper.schooltime
import os
from SHUhelper import app
classroom_dict = {}
json_file = open(os.path.join(app.root_path, 'classroomdata.json'))
classroom_dict = json.load(json_file)

def is_room_empty(room,week,day,time):
    return classroom_dict[room][week][day][time]==1

def get_emptyroom_now():
    week = SHUhelper.schooltime.this_week()
    day = SHUhelper.schooltime.this_day()
    time = SHUhelper.schooltime.this_class()
    return get_emptyroom(week,day,time)

def get_emptyroom(week,day,time):
    emptyroom_list=[]
    if time == 0 or day == 0 or day == 6:
        return emptyroom_list
    for classroom in classroom_dict.keys():
        if classroom_dict[classroom][week-1][day-1][time-1] == 1:
            emptyroom_list.append(classroom)
    return sorted(emptyroom_list)

# print(get_emptyroom_now())

