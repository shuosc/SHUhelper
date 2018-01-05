import re

from flask import Blueprint, current_app, jsonify, request

from UHE.calendar.models import Activity, Event
from UHE.extensions import redis_store
from UHE.plugins import UHEPlugin
from UHE.plugins.SHU_course.models import CourseOfTerm
from UHE.time import Time
import json
from .empty_room import EmptyRoom
from .api import empty_room

# from celery.contrib.methods import task_method
__plugin__ = "SHUEmptyRoom"

cn_num = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
}


class SHUEmptyRoom(UHEPlugin):
    settings_key = 'SHU_emptyrooom'

    def list_init(self):
        semester_list = []
        for i in range(0, 10):
            semester_list.append([([1] * 13) for i in range(0, 5)])
        return semester_list

    def get_classroom_dict(self, term):
        classroom_dict = {}
        courses = CourseOfTerm.objects(term=term)
        for course in courses:
            if not course:
                continue
            raw_time = course.time
            classroom = course.place
            campus = course.campus
            if re.search(r'^([A-G]|[A-G]J)[0-9][0-9][0-9]$', classroom, flags=0) is None and classroom != '':
                if classroom[0] in ['另', '合', '学', '打', '机', '校', '游', '第', '绘', '训', 'I', 'K', '不', '企', '咨', '篮', '网', '体', '排', '足', '']:
                    continue
            if campus not in classroom_dict:
                classroom_dict[campus] = {}
            if classroom not in classroom_dict[campus]:
                classroom_dict[campus][classroom] = self.list_init()
            while True:
                # noinspection Annotator,Annotator,Annotator,Annotator
                time = re.search(
                    r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*', raw_time, flags=0)
                if time is None:
                    break
                # noinspection Annotator,Annotator,Annotator,Annotator
                raw_time = re.sub(
                    r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*', '', raw_time, 1)
                day = cn_num[time.group(1)]
                start = int(time.group(2))
                end = int(time.group(3))
                for week in range(1, 11):
                    in_this_week = False
                    if time.group(4) is not None:
                        if time.group(4) == '单':
                            if week % 2 == 1:
                                in_this_week = True
                        else:
                            if week % 2 == 0:
                                in_this_week = True
                    elif time.group(5) is not None:
                        if int(time.group(5)) <= week <= int(time.group(6)):
                            in_this_week = True
                    elif time.group(7) is not None:
                        if week == int(time.group(7)) or week == int(time.group(8)):
                            in_this_week = True
                    else:
                        in_this_week = True
                    if in_this_week:
                        for i in range(start, end + 1):
                            classroom_dict[campus][classroom][week -
                                                              1][day - 1][i - 1] = 0
        return json.dumps(classroom_dict)

    def setup(self, app):
        print('setup', __plugin__)
        current_app.register_blueprint(empty_room, url_prefix='/empty-room')
        this_term = Time().term_string()
        classroom_dict = redis_store.get('empty_room:' + this_term)
        if classroom_dict is None:
            print('getting _classroom_dict')
            classroom_dict = self.get_classroom_dict(this_term)
            redis_store.set('empty_room:' + this_term, classroom_dict)
        # find_empty_room = EmptyRoom(classroom_dict)

    def install(self, app):
        this_term = Time().term_string()
        classroom_dict = self.get_classroom_dict(this_term)
        if redis_store.get('empty_room:' + this_term) is not None:
            redis_store.delete('empty_room:' + this_term)
        redis_store.set('empty_room:' + this_term, classroom_dict)
        # find_empty_room = EmptyRoom(classroom_dict)

    def uninstall(self):
        print('uninstall')
