"""
Add academic term and basic schduled task to calender
"""

import datetime

from UHE.calendar.models import Activity, Event
from UHE.plugins import UHEPlugin
from UHE.extensions import celery
# from celery.contrib.methods import task_method
__plugin__ = "SHUCalendar"

date = datetime.datetime
delta = datetime.timedelta


class SHUCalendar(UHEPlugin):
    settings_key = 'SHU_calendar'

    def setup(self, app):
        self.year = 2017

        print('setup', __plugin__)
        # celery.add_periodic_task(5.0, clock.s('five'))
        # plugin = Plugin.objects(name=)
        # self.register_blueprint(portal, url_prefix="/portal")
        # connect_event("before-first-navigation-element", inject_portal_link)

    def install(self, app):
        self.main_install()
        print('install school_term_%s success' % (self.year))
        # app.update_func['term_2017'] = self.SHU_calendar_update

    def main_install(self):
        self.event = Event.objects(
            identifier="SHU_calendar_%s" % (self.year)).first()
        if self.event == None:
            self.event = Event(identifier='SHU_calendar_%s' % (self.year),
                               title='上海大学%s-%s学年校历' % (self.year, self.year + 1))
            self.event.save()
        print('install school_term_%s start' % (self.year))
        if self.event.need_update:
            print('update school_term_%s start' % (self.year))
            Activity.objects(event=self.event).delete()
            print('delete old school_term_%s start' % (self.year))
            self.install_acdemic_year()
            self.install_school_term()
            self.install_school_week()
            self.install_basic_schedule_course()
            self.event.need_update = False
            self.event.save()

    def install_acdemic_year(self):
        if self.year == 2017:
            sub_event = Activity(title='上海大学%s-%s学年' % (self.year, self.year + 1),
                                 key='year', args=str(self.year), category='school_calendar',
                                 start=datetime.datetime(2017, 9, 4),
                                 end=datetime.datetime(2018, 8, 27),
                                 event=self.event)
            sub_event.save()

    def install_school_term(self):
        if self.year == 2017:
            terms = (((2017, 9, 4), (2017, 12, 11)),
                     ((2017, 12, 11), (2018, 3, 26)),
                     ((2018, 3, 26), (2018, 6, 18)),
                     ((2018, 6, 18), (2018, 8, 27)))
            term_names = ('秋季学期', '冬季学期', '春季学期', '夏季学期')
            for i in range(4):
                Activity(title='上海大学{}-{}学年{}'.format(self.year, self.year + 1, term_names[i]),
                         key='term', args='{}_{}'.format(self.year, i + 1), category='school_calendar',
                         start=datetime.datetime(
                             terms[i][0][0], terms[i][0][1], terms[i][0][2]),
                         end=datetime.datetime(
                             terms[i][1][0], terms[i][1][1], terms[i][1][2]),
                         event=self.event).save()

    @staticmethod
    def create_week(*start, start_week, end_week, term, key_prefix):
        week_events = []
        for i in range(start_week, end_week):
            week = {'start': date(*start) + delta(days=i * 7),
                    'end': date(*start) + delta(days=(i + 1) * 7),
                    'title': term + '第%s周' % (i + 1),
                    'key': 'week',
                    'args': '{}_{}'.format(key_prefix, i + 1)}
            week_events.append(week)
        return week_events

    def weeks(self):
        if self.year == 2016:
            weeks_of_year = self.create_week(2016, 9, 5, start_week=0, end_week=12, term="2016-2017学年秋季学期", key_prefix="2016_1") + \
                self.create_week(2016, 11, 28,  start_week=0, end_week=6, term="2016-2017学年冬季学期", key_prefix="2016_2") + \
                self.create_week(2017, 2, 13, start_week=6, end_week=12, term="2016_2017学年冬季学期", key_prefix="2016_2") + \
                self.create_week(2017, 3, 27,  start_week=0, end_week=12, term="2016-2017学年春季学期", key_prefix="2016_3") + \
                self.create_week(2017, 6, 19,  start_week=0, end_week=4,
                                 term="2016-2017学年夏季学期", key_prefix="2016_4")
        elif self.year == 2017:
            weeks_of_year = self.create_week(2017, 9, 11, start_week=0, end_week=9, term="2017-2018学年秋季学期", key_prefix="2017_1") + \
                self.create_week(2017, 11, 20,  start_week=9, end_week=12, term="2017-2018学年秋季学期", key_prefix="2017_1") + \
                self.create_week(2017, 12, 11,  start_week=0, end_week=8, term="2017-2018学年冬季学期", key_prefix="2017_2") + \
                self.create_week(2018, 2, 5, start_week=8, end_week=12, term="2017_2018学年冬季学期", key_prefix="2017_2") + \
                self.create_week(2018, 3, 26,  start_week=0, end_week=12, term="2017-2018学年春季学期", key_prefix="2017_3") + \
                self.create_week(2018, 6, 18,  start_week=0, end_week=4,
                                 term="2017-2018学年夏季学期", key_prefix="2017_4")
        return weeks_of_year

    def install_school_week(self):
        if self.year == 2017:
            weeks = self.weeks()
            for week in weeks:
                schedule_event = Activity(
                    start=week['start'], end=week['end'],
                    title=week['title'], key=week['key'],
                    category='school_calendar', args=week['args'], event=self.event)
                schedule_event.save()

    def course_subevent(self, day, weekday, title, args):
        times = [(8, 0), (8, 55), (10, 0), (10, 55), (12, 10), (13, 5),
                 (14, 10), (15, 5), (16, 0), (16, 55), (18, 0), (18, 55), (19, 50)]
        for i in range(12):
            start_delta = delta(hours=times[i][0], minutes=times[i][1])
            end_delta = delta(
                hours=times[i][0], minutes=times[i][1]) + delta(minutes=45)
            course_event = {
                'start': day + start_delta,
                'end': day + end_delta,
                'title': title,
                'key': 'course_basic',
                'args': '{}_{}_{}'.format(args, weekday + 1, i + 1),
                'event': self.event,
                'category': 'school_calendar',
                'visible': 'private'
            }
            Activity(**course_event).save()

    def install_basic_schedule_course(self):
        weeks = self.weeks()
        for week in weeks:
            for day in range(5):
                self.course_subevent(
                    week['start'] + delta(days=day), day, week['title'], week['args'])

    def update_func(self):
        print('update func call')

    def uninstall(self):
        print('uninstall')
        print('miao')
        event = Event.objects(
            identifier="SHU_calendar_%s" % (year)).first()
        Activity.objects(event=event).delete()
        event.delete()
        # delete_settings_from_fixture(fixture)

# @celer.task()
# def async_install():
