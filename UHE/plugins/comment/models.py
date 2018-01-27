import datetime

from mongoengine import (DateTimeField, ListField, CASCADE, PULL,
                         ReferenceField, StringField, GenericReferenceField)

# from config import db
from UHE.extensions import db
from UHE.user.models import User


# from UHE.feed.models import Feed

class Comment(db.Document):
    post = GenericReferenceField()
    user = ReferenceField(User,  reverse_delete_rule=CASCADE)
    content = StringField(default='')
    liked = ListField(ReferenceField(User, deref=True,
                                     reverse_delete_rule=PULL), default=lambda: [])
    created = DateTimeField(default=datetime.datetime.now)
    meta = {
        'ordering': ['created'],
        'strict': False
    }

    def __unicode__(self):
        return self.content

    def to_dict(self):
        return {
            'user': self.user.to_dict_public(),
            'created': str(self.created),
            'content': self.content,
            'id': str(self.id)
        }
