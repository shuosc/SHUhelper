import datetime
import time
from UHE.calendar.models import Activity


class Time():
    def __init__(self, date=datetime.datetime.now()):
        self.date = date

    def year(self):
        year_event = Activity.objects(
            start__lte=self.date, end__gte=self.date, key='year').first()
        if year_event is not None:
            return int(year_event.args.split('_')[-1])
        else:
            return 0

    def week(self):
        week_event = Activity.objects(
            start__lte=self.date, end__gte=self.date, key='week').first()
        if week_event is not None:
            return int(week_event.args.split('_')[-1])
        else:
            return 0

    def term(self):
        term_event = Activity.objects(
            start__lte=self.date, end__gte=self.date, key='term').first()
        if term_event is not None:
            return int(term_event.args.split('_')[-1])
        else:
            return 0
    
    def term_string(self):
        return str(self.year()) + '_' + str(self.term())

    def day(self):
        return int(time.strftime("%w"))

    # def course(self):
    #     course_event = Activity.objects(
    #         start__lte=self.date-datetime.timedelta(minutes=30), end__gte=self.date, key='course_basic').first()
    #     if course_event is not None:
    #         return int(course_event.args.split('_')[-1])
    #     else:
    #         return 0
    def course(self):
        ctime = int(time.strftime("%H%M"))
        if ctime <= 800:
            return 0
        elif ctime <= 845:
            return 1
        elif ctime <= 940:
            return 2
        elif ctime <= 1045:
            return 3
        elif ctime <= 1140:
            return 4
        elif ctime <= 1255:
            return 5
        elif ctime <= 1350:
            return 6
        elif ctime <= 1455:
            return 7
        elif ctime <= 1550:
            return 8
        elif ctime <= 1645:
            return 9
        elif ctime <= 1740:
            return 10
        elif ctime <= 1845:
            return 11
        elif ctime <= 1940:
            return 12
        elif ctime <= 2035:
            return 13
        else:
            return 0

    def time_tuple(self):
        return (self.year(), self.term(), self.week(), self.day(), self.course())
