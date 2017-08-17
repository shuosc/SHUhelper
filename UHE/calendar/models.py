from mongoengine import (BooleanField, DateTimeField, ListField, ReferenceField, StringField)
import mongoengine
from mongoengine import (BooleanField, DateTimeField, ListField, ReferenceField, StringField)

# from config import db
from UHE.comment.models import Comment
from UHE.extensions import db, celery
from UHE.user.models import User


# class Comment(db.EmbeddedDocument):
#     user = ReferenceField(User)
#     content = StringField()
#     liked = IntField()
#     create_time = DateTimeField(datetime.datetime.now)


class Event(db.Document):
    user = ReferenceField(User)
    identifier = StringField(unique=True)
    title = StringField(default=lambda: '')
    remark = StringField(default=lambda: '')
    meta = {'strict': False}
    need_update = BooleanField(default=True)
    liked = ListField(ReferenceField(User), default=lambda: [])
    comments = ListField(ReferenceField(Comment), default=lambda: [])
    attend = ListField(ReferenceField(User), default=lambda: [])

    def to_dict(self):
        return {
            'user':
            {
                'name': self.user.display_name, 'card_id': self.user.card_id
            },
            'start': str(self.start_time),
            'end': str(self.end_time),
            'title': self.title,
            'content': self.content,
            'place': self.place,
            'type': self.event_type
        }

    def __unicode__(self):
        return self.identifier


# class BaseSubEvent(db.Document):
#     event = ReferenceField(Event)
#     title = StringField()
#     task_start_id = StringField()
#     task_end_id = StringField()
#     key = StringField()
#     expired = BooleanField()


# class RepeatSubEvent(BaseSubEvent):
#     range_start = DateTimeField()
#     range_end = DateTimeField()
#     start_hours = IntField()
#     start_minutes = IntField()
#     end_hours = IntField()
#     end_minutes = IntField()
#     working_day = BooleanField(default=False)
#     repeat_day = IntField(default=0b1111111)
#     repeat_week = IntField(default=0b111111111111)
#     schedule_day = DateTimeField()


#     @classmethod
#     def pre_save(cls, sender, document, **kwargs):
#         if document.key != None:
#             task_start = signal_scheduler.apply_async(
#                 args=[document.key + '_start', document], eta=document.range_start)
#             task_end = signal_scheduler.apply_async(
#                 args=[document.key + '_end', document], eta=document.range_end)
#             document.task_start_id = task_start.id
#             document.task_end_id = task_end.id

#     @classmethod
#     def pre_delete(cls, sender, document, **kwargs):
#         if document.key != None:
#             celery.control.revoke(document.task_start_id)
#             celery.control.revoke(document.task_end_id)


# mongoengine.signals.pre_save.connect(
#     RepeatSubEvent.pre_save, sender=RepeatSubEvent)
# mongoengine.signals.pre_delete.connect(
#     RepeatSubEvent.pre_delete, sender=RepeatSubEvent)


class Activity(db.Document):
    category = StringField()
    # system school_calendar opening_schedule school-activaties confrence club-activaties  acdemic course
    event = ReferenceField(Event)
    title = StringField()
    place = StringField()
    visible = StringField(default='public')
    task_start_id = StringField()
    task_end_id = StringField()
    key = StringField()  # send singal and find event precisily
    # like year term week course_basic course etc
    args = StringField()  # singal args
    start = DateTimeField(required=True)
    end = DateTimeField(required=True)
    meta = {'ordering': ['start'], 'strict': False}

    # def find_schedule_day(self):
    #     now = datetime.datetime.now()
    #     now.second = 0
    #     now.microsecond = 0
    #     datetime.timedelta()
    #     if self.range_end < now:
    #         days = (now - range_end).days
    #         for i in range(days):
    #             schedule_day = now + datetime.timedelta(days=i)
    #             week = find_week_binary(schedule_day)
    #             day = find_day_binary(schedule_day)
    #             if week & self.repeat_week and day & self.repeat_day:
    #                 return schedule_day
    #     return None
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if document.key != None:
            pass
            # now = datetime.datetime.now()
            # now.second = 0
            # now.microsecond = 0
            # if document.start
            # task_start = signal_scheduler.apply_async(
            #     args=[document.key + '_start', '1'], eta=document.start)
            # # print('apply_async finish')
            # task_end = signal_scheduler.apply_async(
            #     args=[document.key + '_end', '1'], eta=document.end)
            # document.task_start_id = task_start.id
            # document.task_end_id = task_end.id

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        if document.task_start_id:
            celery.control.revoke(document.task_start_id)
        if document.task_end_id:
            celery.control.revoke(document.task_end_id)


mongoengine.signals.pre_save.connect(
    Activity.pre_save, sender=Activity)
mongoengine.signals.pre_delete.connect(
    Activity.pre_delete, sender=Activity)
