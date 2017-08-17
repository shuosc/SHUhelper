
from UHE.message.models import Message,Conversation
from UHE.user.models import User

def create_application_message(sender,receiver,message_text):
    message = Message(user=sender,message_type='application',message=message_text)
    message.save()
    conversation = Conversation.objects(to_user=receiver).first()
    if conversation == None:
        conversation =  Conversation(from_user=sender,to_user=user)
    conversation.messages.append(message)
    conversation.save()

def create_system_message(sender,receiver,message_text):
    message = Message(user=sender,message_type='system',message=message_text)
    message.save()
    receivers = User.objects(is_robot=False,is_activated=True)
    for receiver in receivers:
        conversation = Conversation.objects(to_user=receiver).first()
        if conversation == None:
            conversation =  Conversation(from_user=sender,to_user=user)
        conversation.messages.append(message)
        conversation.save()