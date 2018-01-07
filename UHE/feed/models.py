import datetime

from mongoengine import (DateTimeField, IntField, PULL, NULLIFY, CASCADE,BooleanField,DictField,EmbeddedDocumentField,
                         ListField, ReferenceField, StringField)
from flask_login import current_user
from UHE.extensions import db
# from config import db
from UHE.user.models import User
# from UHE.comment.models import Comment

class Comment(db.EmbeddedDocument):
    user = ReferenceField(User)
    text = StringField(default='')
    liked = ListField(ReferenceField(User, deref=True), default=lambda: [])
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
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    display_name = StringField()
    created = DateTimeField(default=datetime.datetime.now)
    # comments = ListField(ReferenceField(
    #     Comment, reverse_delete_rule=PULL), default=lambda: []) #deprecated
    comment_list = ListField(EmbeddedDocumentField(Comment))
    namespace = StringField(default='ordinary')  # external-link internal-link imgs text post
    text = StringField(default='')
    link = DictField()
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
            'comments': [comment.to_dict() for comment in self.comment_list],
            'namespace': self.namespace,
            'text': self.text,
            'img': self.img,
            'like': self.like,
            'id': str(self.id),
            'liked': current_user.id in list(map(lambda user: user.id, self.like)),
            'likecount': len(self.like)
        }
