import datetime

import mongoengine
from flask_login import current_user
from mongoengine import (BooleanField, DateTimeField, CASCADE,
                         ListField, ReferenceField, StringField)

from UHE.extensions import db
from UHE.user.models import User


# from config import db


class Message(db.Document):
    sender = ReferenceField(User, reverse_delete_rule=CASCADE)
    sort = StringField(choices=('system', 'application', 'private'))
    content = StringField()
    read = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    expire_from = DateTimeField(default=lambda: datetime.datetime(2100, 1, 1))
    meta = {
        'indexes': [
            {'fields': ['expire_from'], 'expireAfterSeconds': 3600 * 24 * 7}
        ],
        'strict': False
    }

    def to_dict(self):
        return {
            'created': str(self.created),
            'sender': self.sender.card_id,
            'content': self.content
        }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if document.sort == 'private' and document.read:
            document.expire_from = datetime.datetime.now()

    def __unicode__(self):
        return self.content
    #  @classmethod
    #  def pre_delete(cls, sender, document, **kwargs):
    #      sender_dialog = Dialog.objects(contact=document.sender)
    #      receiver_dialog = Dialog.objects(contact=document.receiver)
    #      sender


class Conversation(db.Document):
    members = ListField(ReferenceField(User, reverse_delete_rule=PULL))
    messages = ListField(ReferenceField(
        Message, reverse_delete_rule=mongoengine.PULL, default=lambda: []))
    deleted = BooleanField(default=False)

    # unreadmessages = ListField(ReferenceField(
    #     Message, reverse_delete_rule=mongoengine.PULL, default=lambda: []))
    meta = {'strict': False}
    conversation_type = StringField(
        choices=('system', 'application', 'private'))
    # def get_messages(count):

    @property
    def first_message(self):
        """Returns the first message object."""
        return self.messages[0]

    def get_unread(self):
        return [message.to_dict() for message in self.unreadmessages]

    @property
    def last_message(self):
        """Returns the last message object."""
        if len(self.messages):
            return self.messages[-1]
        else:
            return None

    def to_dict_abstract(self):
        data = {'id': str(self.id), 'conversation': str(self.id)}
        if current_user.id == self.from_user.id:
            data['fromUser'] = self.from_user.to_dict()
            data['toUser'] = self.to_user.to_dict()
        else:
            data['toUser'] = self.from_user.to_dict()
            data['fromUser'] = self.to_user.to_dict()
        # if len(self.unreadmessages) == 0:
        data['lastMessage'] = self.last_message.to_dict(
        ) if self.last_message is not None else None
        # else:
        #     data['unread'] = len(self.unreadmessages)
        return data

    def to_dict_detail(self):
        data = {'conversation': str(self.id)}
        if current_user.id == self.from_user.id:
            data['fromUser'] = self.from_user.to_dict()
            data['toUser'] = self.to_user.to_dict()
        else:
            data['toUser'] = self.from_user.to_dict()
            data['fromUser'] = self.to_user.to_dict()
        # data['messages'] = [message.to_dict()
        #                     for message in self.messages[-10:]]
        data['id'] = str(self.id)
        data['count'] = len(self.messages)
        return data

    # @classmethod
    # def pre_save(cls,sender, document, **kwargs):
    #     print(document)
    #     if len(document.messages):
    #         document.delete()


class UserContact(db.Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    contact = ReferenceField(User, reverse_delete_rule=CASCADE)
    conversation = ReferenceField(Conversation)
    unread_messges_count = IntField()
    last_open = DateTimeField()
    avatar = StringField()
    title = StringField()


mongoengine.signals.pre_save.connect(Message.pre_save, sender=Message)
