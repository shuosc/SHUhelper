import datetime
from flask_login import current_user
from application.extensions import db
from application.models.user import User
from sqlalchemy.dialects import postgresql


class Event(db.Model):
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    author_id = db.Column(db.String, db.ForeignKey('user.id'))
    tags = db.Column(postgresql.ARRAY(db.String, dimensions=1))
    title = db.Column(db.String)
    namespace = db.Column(db.String)
    content = db.Column(db.String)
    type = db.Column(db.String)
    hit = db.Column(db.Interger, default=0)
    # liked = ListField(ReferenceField(
    #     User, reverse_delete_rule=PULL), default=lambda: [])
    participants = db.relationship('EventParticipate', lazy='select',
                                backref=db.backref('event', lazy=True))
    __mapper_args__ = {
       'polymorphic_identity': 'normal',
        'polymorphic_on': type
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

class CourseEvent(Event):
    __tablename__ = 'course_event'
    course_id = db.Column(db.String, db.ForeignKey('user.id'))
    class_id = db.Column(db.String, db.ForeignKey('user.id'))
    color = db.Column(db.String, db.ForeignKey('user.id'))
    year = db.Column(db.Integer)
    term = db.Column(db.Integer)
     __mapper_args__ = {
       'polymorphic_identity': 'course'
     }

class EventParticipate(db.Model):
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    event_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('event.id'))
    participant = db.Column(db.String, db.ForeignKey('user.id'))
    color = db.Column(db.String, db.ForeignKey('user.id'))
    remark = db.Column(db.String)

class EventInstance(db.Model):
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    event_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('event.id'))
    title = db.Column(db.String)
    place = db.Column(db.String)
    key = StringField()  # send signal and find event
    # like year term week course_basic course etc
    args = StringField()  # machine readble text, use for signal args
    start = DateTimeField(required=True)
    end = DateTimeField(required=True)

    def to_dict(self):
        return {
            'args': self.args,
            'start': self.start.timestamp(),
            'end': self.end.timestamp(),
            'title': self.title,
            'visible': self.visible,
            'category': self.category,
            'place': self.place,
            'key': self.key,
            'id': str(self.id),
            'event_id': str(self.event)
        }

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
