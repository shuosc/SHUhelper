import datetime
from flask_login import current_user
from application.extensions import db
from application.models.user import User


class Conversation(db.Model):
    id = db.Column(db.UUID(as_uuid=True),default=uuid.uuid4, primary_key=True)
    members = ListField(ReferenceField(User, reverse_delete_rule=PULL))
    messages = ListField(ReferenceField(
        Message, reverse_delete_rule=mongoengine.PULL, default=lambda: []))
    deleted = BooleanField(default=False)
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
class UserContact(db.Model):
    user =  db.Column(db.String, db.ForeignKey('user.id'))
    contact = db.Column(db.String, db.ForeignKey('user.id'))
    conversation =  db.Column(db.UUID, db.ForeignKey('conversation.id'))
    unread_messges_count = IntField()
    last_open = DateTimeField()
    avatar = StringField()
    title = StringField()

class ConversationMember(db.Model):
    id = db.Column(db.UUID(as_uuid=True),default=uuid.uuid4, primary_key=True)
    conversation_id = db.Column(db.UUID, db.ForeignKey('conversation.id'))
    member = db.Column(db.String, db.ForeignKey('user.id'))
    avatar_URL = db.Cloumn(db.String)
    status = db.Cloumn(db.String)
    created = DateTimeField(default=datetime.datetime.now)
    last_open = 

class ConversationMessage(db.Model):
    id = db.Column(db.UUID(as_uuid=True),default=uuid.uuid4, primary_key=True)
    conversation_id = db.Column(db.UUID, db.ForeignKey('conversation.id'))
    from_user_id = db.Column(db.String, db.ForeignKey('user.id'))
    content = db.Column(db.String)
    read = db.Column(db.Boolean,default=False)
    created = DateTimeField(default=datetime.datetime.now)
    # expire_from = DateTimeField(default=lambda: datetime.datetime(2100, 1, 1))

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

