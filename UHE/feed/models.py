import datetime

from mongoengine import (DateTimeField, IntField, PULL, NULLIFY, CASCADE,
                         ListField, ReferenceField, StringField)
from flask_login import current_user
from UHE.extensions import db
# from config import db
from UHE.user.models import User
from UHE.comment.models import Comment


class Feed(db.Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    display_name = StringField()
    created = DateTimeField(default=datetime.datetime.now)
    comments = ListField(ReferenceField(
        Comment, reverse_delete_rule=PULL), default=lambda: [])
    namespace = StringField(default='ordinary')  # external-link internal-link imgs text post
    text = StringField(default='')
    link_URL = StringField()
    link_title = StringField()
    link_img = StringField()
    img = ListField(StringField())
    like = ListField(ReferenceField(User,reverse_delete_rule=PULL, deref=True), default=lambda: [])
    meta = {
        'ordering': ['-created'],
        'strict': False
    }

    def __unicode__(self):
        return self.text

    def to_dict(self):
        # print(current_user.id,list(map(lambda user: user.id,self.like)))
        return {
            'user': self.user.to_dict_public(),
            'displayName': self.display_name,
            'created': str(self.created),
            'comments': [comment.to_dict() for comment in self.comments],
            'namespace': self.namespace,
            'text': self.text,
            'linkURL': self.link_URL,
            'linkTitle': self.link_title,
            'linkImg': self.link_img,
            'img': self.img,
            'like': self.like,
            'id': str(self.id),
            'liked': current_user.id in list(map(lambda user: user.id, self.like)),
            'likecount': len(self.like)
        }
