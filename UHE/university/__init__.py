import datetime

from UHE.calendar.models import Activity


class University():
    def __init__(self):
        self.semester = ''
        self.vacation = True
        self.vacation_name = 'summer'
        self.name = '上海大学'

    def this_year(self):
        year_event = Activity.objects(
            start__gte=date, end__lte=date, key='year').first()
        if year_event != None:
            return int(year_event.args)
        else:
            return 0

    def this_week(self, date=datetime.datetime.now()):
        week_event = Activity.objects(
            start__gte=date, end__lte=date, key='week').first()
        if week_event != None:
            return int(week_event.args)
        else:
            return 0

    def this_term(self, date=datetime.datetime.now()):
        term_event = Activity.objects(
            start__gte=date, end__lte=date, key='term').first()
        if term_event != None:
            return int(term_event.args)
        else:
            return 0

    def this_course(self, date=datetime.datetime.now()):
        course_event = Activity.objects(start__gte=date,end__lte=date,key='course_basic').first()
        if course_event != None:
            return int(course_event.args)
        else:
            return 0
    def on_vacation(self):
        return True

    def is_working_day(self):
        return True

    def this_day(self):
        return

    def this_time(self):
        return
