import datetime
from .models import Activity

class Time():
    def __init__(self, now=datetime.datetime.now()):
        self.now = now
        self.__year_expire = now
        self.__term_expire = now
        self.__week_expire = now
        self.refresh()
    
    def refresh(self):
        self.year,self.__year_expire = self.get_year()
        self.term,self.__term_expire  = self.get_term()
        self.day = self.get_day()
        self.week,self.__week_expire  = self.get_week()
        self.course = self.get_course()
    
    @property
    def time(self):
        self.refresh()
        return self
    
    @property
    def term_string(self):
        time = self.time
        return str(time.year) + '_' + str(time.term)
    
    def get_year(self):
        if self.now < self.__year_expire:
            return self.year,self.__year_expire
        year_event = Activity.objects(
            start__lte=self.now, end__gte=self.now, key='year').first()
        if year_event is not None:
            return int(year_event.args.split('_')[-1]),year_event.end
        else:
            return 0,self.now

    def get_week(self):
        if self.now < self.__week_expire:
            return self.week,self.__week_expire
        week_event = Activity.objects(
            start__lte=self.now, end__gte=self.now, key='week').first()
        if week_event is not None:
            return int(week_event.args.split('_')[-1]),week_event.end
        else:
            return 0,self.now

    def get_term(self):
        if self.now < self.__term_expire:
            return self.term,self.__term_expire
        term_event = Activity.objects(
            start__lte=self.now, end__gte=self.now, key='term').first()
        if term_event is not None:
            return int(term_event.args.split('_')[-1]),term_event.end
        else:
            return 0,self.now


    def get_day(self):
        return int(self.now.strftime("%w")) if int(self.now.strftime("%w")) != 0 else 7

    # def course(self):s
    #     course_event = Activity.objects(
    #         start__lte=self.date-datetime.timedelta(minutes=30), end__gte=self.date, key='course_basic').first()
    #     if course_event is not None:
    #         return int(course_event.args.split('_')[-1])
    #     else:
    #         return 0
    def get_course(self):
        ctime = int(self.now.strftime("%H%M"))
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
