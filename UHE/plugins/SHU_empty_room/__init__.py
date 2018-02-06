import json
import re

from flask import current_app

from UHE.extensions import redis_store
from UHE.plugins import UHEPlugin
from UHE.plugins.SHU_course.models import CourseOfTerm
from .api import empty_room
from .empty_room import EmptyRoom

# from celery.contrib.methods import task_method
__plugin__ = "SHUEmptyRoom"

CN_NUM = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
}

R_CLASSROOM = r'^([A-G]|[A-G]J)[0-9][0-9][0-9]$'
R_COURSE_TIME = r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*'
NOT_CLASSROOM_TUPLE = ('另', '合', '学', '打', '机', '校', '游', '第',
                       '绘', '训', 'I', 'K', '不', '企', '咨', '篮', '网', '体', '排', '足', '')


class SHUEmptyRoom(UHEPlugin):
    settings_key = 'SHU_emptyrooom'

    def list_init(self):
        semester_list = []
        for i in range(0, 10):
            semester_list.append([([1] * 13) for i in range(0, 5)])
        return semester_list

    def in_this_week(self,time,week):
        in_this_week = False
        if time.group(4) is not None:
            in_this_week = week % 2 == (time.group(4) == '单')
        elif time.group(5) is not None:
            in_this_week = int(time.group(
                5)) <= week <= int(time.group(6))
        elif time.group(7) is not None:
            in_this_week = week == int(time.group(7)) or week == int(time.group(8)):
        else:
            in_this_week = True
        return in_this_week

    def set_classroom(self, raw_time, classroom_dict):
        while True:
            time = re.search(R_COURSE_TIME, raw_time, flags=0)
            if time is None:
                break
            raw_time = re.sub(R_COURSE_TIME, '', raw_time, 1)
            day = CN_NUM[time.group(1)]
            start = int(time.group(2))
            end = int(time.group(3))
            for week in range(1, 11):
                if self.in_this_week(time,week):
                    for i in range(start, end + 1):
                        classroom_dict[week -1][day - 1][i - 1] = 0

    def get_classroom_dict(self, term):
        classroom_dict = {}
        courses = CourseOfTerm.objects(term=term)
        for course in courses:
            if not course:
                continue
            raw_time = course.time
            classroom = course.place
            campus = course.campus
            if re.search(R_CLASSROOM, classroom, flags=0) is None and classroom != '':
                if classroom[0] in NOT_CLASSROOM_TUPLE:
                    continue
            if campus not in classroom_dict:
                classroom_dict[campus] = {}
            if classroom not in classroom_dict[campus]:
                classroom_dict[campus][classroom] = self.list_init()
            self.set_classroom(raw_time, classroom_dict[campus][classroom])
        return json.dumps(classroom_dict)

    def setup(self, app):
        print('setup', __plugin__)
        current_app.register_blueprint(empty_room, url_prefix='/empty-room')
        this_term = current_app.school_time.term_string
        classroom_dict = redis_store.get('empty_room:' + this_term)
        if classroom_dict is None:
            print('getting _classroom_dict')
            classroom_dict = self.get_classroom_dict(this_term)
            redis_store.set('empty_room:' + this_term, classroom_dict)
        # find_empty_room = EmptyRoom(classroom_dict)

    def install(self, app):
        this_term = current_app.school_time.term_string
        classroom_dict = self.get_classroom_dict(this_term)
        if redis_store.get('empty_room:' + this_term) is not None:
            redis_store.delete('empty_room:' + this_term)
        redis_store.set('empty_room:' + this_term, classroom_dict)
        # find_empty_room = EmptyRoom(classroom_dict)

    def uninstall(self):
        print('uninstall')
