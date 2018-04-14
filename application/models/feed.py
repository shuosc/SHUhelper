import datetime

from flask_login import current_user
from mongoengine import (DateTimeField, IntField, PULL, CASCADE, BooleanField, DictField, EmbeddedDocumentField,
                         ListField, ReferenceField, StringField)

from application.extensions import db
from application.user.models import User

class Comment(db.EmbeddedDocument):
    author = ReferenceField(User)
    text = StringField(default='')
    liked = ListField(ReferenceField(User, deref=True), default=lambda: [])
    liked_count = IntField()
    reply = IntField(default=-1)
    deleted = BooleanField(default=False)
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
            'text': self.text
        }

class Feed(db.Document):
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    display_name = StringField()
    created = DateTimeField(default=datetime.datetime.now)
    comments = ListField(EmbeddedDocumentField(Comment))
    namespace = StringField(default='ordinary')  # external-link internal-link imgs text post
    content = StringField(default='')
    tags = ListField(StringField)
    link = DictField()
    img = ListField(StringField())
    hits = IntField(default=0)
    liked = ListField(ReferenceField(User,reverse_delete_rule=PULL, deref=True), default=lambda: [])
    liked_count = IntField(default=0)
    deleted = BooleanField(default=False)
    meta = {
        'ordering': ['-created'],
        'strict': False
    }

    def __unicode__(self):
        return self.text


    def increase_hit(self):
        self.hits += 1

    def to_dict(self):
        # print(current_user.id,list(map(lambda user: user.id,self.like)))
        return {
            'user': self.user.to_dict_public(),
            'displayName': self.display_name,
            'created': str(self.created),
            'comments': [comment.to_dict() for comment in self.comment_list],
            'namespace': self.namespace,
            'text': self.text,
            'deleted': self.deleted,
            'img': ['https://static.shuhelper.cn/' + img for img in self.img],
            'like': [user.to_dict_public() for user in self.like],
            'id': str(self.id),
            'hits': self.hits,
            'liked': current_user.id in list(map(lambda user: user.id, self.like)),
            'likecount': len(self.like)
        }
