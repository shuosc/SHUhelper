import datetime

from mongoengine import (DateTimeField, IntField, ListField, ReferenceField, StringField)

from UHE.extensions import db
# from config import db
from UHE.user.models import User


class Feed(db.Document):
    user = ReferenceField(User)
    created = DateTimeField(default=datetime.datetime.now)
    comments = IntField(default=0)
    feed_type = StringField()  # external-link internal-link imgs text post
    text = StringField()
    link_URL = StringField()
    link_title = StringField()
    link_img = StringField()
    img = ListField(StringField())
    like = ListField(ReferenceField(User,deref=True),default=lambda:[])
    meta = {
        'ordering': ['-created'],
        'strict': False
    }

    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'created': str(self.created),
            'comments': self.comments,
            'type': self.feed_type,
            'text': self.text,
            'linkURL': self.link_URL,
            'linkTitle': self.link_title,
            'linkImg': self.link_img,
            'img': self.img,
            'like': self.like,
            'id': str(self.id)
        }
