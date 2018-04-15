import datetime

# from .models import Activity

COURSE_SCHEDULE = [800,845,940,1045,1140,1255,1350,1455,1550,1645,1740,1845,1940,2035]

class Time():
    def __init__(self, now=datetime.datetime.now()):
        self.now = now
        self.__year_expire = now
        self.__term_expire = now
        self.__week_expire = now
        self.week = 0
        self.year = 0
        self.course = 0
        self.day = 0
        self.refresh()

    def refresh(self):
        self.now = datetime.datetime.now()
        # self.year, self.__year_expire = self.get_year()
        # self.term, self.__term_expire = self.get_term()
        self.day = self.get_day()
        # self.week, self.__week_expire = self.get_week()
        self.course = self.get_course()

    @property
    def time(self):
        self.refresh()
        return self

    @property
    def term_string(self):
        time = self.time
        return str(time.year) + '_' + str(time.term)

    # def get_year(self):
    #     if self.now < self.__year_expire:
    #         return self.year, self.__year_expire
    #     year_event = Activity.objects(
    #         start__lte=self.now, end__gte=self.now, key='year').first()
    #     if year_event is not None:
    #         return int(year_event.args.split('_')[-1]), year_event.end
    #     else:
    #         return 0, self.now

    # def get_week(self):
    #     if self.now < self.__week_expire:
    #         return self.week, self.__week_expire
    #     week_event = Activity.objects(
    #         start__lte=self.now, end__gte=self.now, key='week').first()
    #     if week_event is not None:
    #         return int(week_event.args.split('_')[-1]), week_event.end
    #     else:
    #         return 0, self.now

    # def get_term(self):
    #     if self.now < self.__term_expire:
    #         return self.term, self.__term_expire
    #     term_event = Activity.objects(
    #         start__lte=self.now, end__gte=self.now, key='term').first()
    #     if term_event is not None:
    #         return int(term_event.args.split('_')[-1]), term_event.end
    #     else:
    #         return 0, self.now

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
        for (index, value) in enumerate(COURSE_SCHEDULE):
            if ctime <= value:
                return index
        if self.now.hour < 8:
            return 0
        if self.now.hour > 20:
            return 14
        
