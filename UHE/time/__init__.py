import datetime
import time
from UHE.calendar.models import Activity


class Time():
    def __init__(self,date=datetime.datetime.now()):
        self.date = date

    def year(self):
        year_event = Activity.objects(
            start__gte=self.date, end__lte=self.date, key='year').first()
        if year_event is not None:
            return int(year_event.args.split('_')[-1])
        else:
            return 0

    def week(self):
        week_event = Activity.objects(
            start__gte=self.date, end__lte=self.date, key='week').first()
        if week_event is not None:
            return int(week_event.args.split('_')[-1])
        else:
            return 0

    def term(self):
        term_event = Activity.objects(
            start__gte=self.date, end__lte=self.date, key='term').first()
        if term_event is not None:
            return int(term_event.args.split('_')[-1])
        else:
            return 0

    def day(self):
        return int(time.strftime("%w"))

    def course(self):
        course_event = Activity.objects(
            start__gte=self.date, end__lte=self.date, key='course_basic').first()
        if course_event is not None:
            return int(course_event.args.split('_')[-1])
        else:
            return 0

    def time_tuple(self):
        return (self.year(), self.term(), self.week(), self.day(), self.course())
