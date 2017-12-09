from flask import Blueprint, jsonify
from UHE.calendar.models import Activity, Event
from UHE.plugins import UHEPlugin
from UHE.plugins.SHU_course.models import CourseOfTerm
from flask import Blueprint, request, current_app

from UHE.calendar.models import Activity, Event
from UHE.plugins import UHEPlugin
from UHE.plugins.SHU_course.models import CourseOfTerm
from UHE.extensions import redis_store
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
        if redis_store.get('empty_room') is None:
            pass


    def install(self, app):
        courses = CourseOfTerm.objects(term='2017_2')
        for course in courses:
            if not course:
                continue
            if course.term != '2017_1':
                continue
            raw_time=course.time
            classroom=course.place
            if re.search(r'^([A-G]|[A-G]J)[0-9][0-9][0-9]$', classroom, flags=0) is None:
                continue
            if classroom not in classroom_dict:
                classroom_dict[classroom] = list_init()
                ff.write(classroom+'\n')
            while True:
                # noinspection Annotator,Annotator,Annotator,Annotator
                time = re.search(r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*',raw_time,flags=0)
                if time is None:
                    break
                # noinspection Annotator,Annotator,Annotator,Annotator
                raw_time = re.sub(r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*','',raw_time,1)
                
                day = cn_num[time.group(1)]
                start = int(time.group(2))
                end = int(time.group(3))
                for week in range(1,11):
                    in_this_week = False
                    if time.group(4) is not None:
                        if time.group(4) == '单':
                            if week%2==1:
                                in_this_week=True
                        else:
                            if week%2==0:
                                in_this_week=True
                    elif time.group(5) is not None:
                        if int(time.group(5)) <= week <= int(time.group(6)):
                            in_this_week=True
                    elif time.group(7) is not None:
                        if week==int(time.group(7)) or week==int(time.group(8)):
                            in_this_week=True
                    else:
                        in_this_week=True
                    if in_this_week:
                        for i in range(start,end+1):
                            classroom_dict[classroom][week-1][day-1][i-1] = 0


    def uninstall(self):
        print('uninstall')
        event = Event.objects(
            identifier="SHU_calendar_%s" % year).first()
        Activity.objects(event=event).delete()
        event.delete()
