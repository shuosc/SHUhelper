from flask import Blueprint, jsonify, request
# from flask_login import current_user.
from flask.views import MethodView
from flask_login import current_user, login_required
from mongoengine.queryset.visitor import Q
import datetime
from UHE.extensions import redis_store
from UHE.message.models import Conversation, Message
from UHE.user.models import User
import json
conversations = Blueprint('conversations', __name__)


@conversations.route('/<conversation_id>/after/<start>')
def after_messages(conversation_id, start):
    messages = redis_store.lrange(
        'conversation_' + conversation_id, int(start), int(start) + 10)
    return jsonify(messages=[json.loads(message) for message in messages])


class ConversationAPI(MethodView):
    decorators = [login_required]

    def get(self, conversation_id=None):
        if not conversation_id:
            conversations = Conversation.objects(
                (Q(to_user=current_user.id)
                 | Q(from_user=current_user.id)))
            return jsonify([conversation.to_dict_abstract() for conversation in conversations])
        else:
            conversation = Conversation.objects.get_or_404(id=conversation_id)
            key = 'conversation_' + str(conversation.id)
            redis_store.delete(key)
            if len(conversation.messages) != 0:
                redis_store.rpush(key, *[message.to_json() for message in conversation.messages])
            return jsonify(conversation.to_dict_detail())

    def post(self):
        args = request.get_json()
        to_user = User.objects(card_id=args['to']).first()
        if to_user is None:
            to_user = User(card_id=args['to'])
            to_user.save()
        else:
            conversation = Conversation.objects(Q(to_user=to_user.id, from_user=current_user.id) | (
                Q(to_user=current_user.id, from_user=to_user.id))).first()
            if conversation is None:
                conversation = Conversation(
                    from_user=current_user.id, to_user=to_user, messages=[])
                conversation.save()
        return jsonify({'id': str(conversation.id)})

    def put(self, conversation_id):
        args = request.get_json()
        message = Message(sender=current_user.id,
                          sort="private", content=args['content'])
        message.save()
        Conversation.objects(id=conversation_id).update_one(
            push__messages=message)
        redis_store.lpush('conversation_' + str(conversation_id), message.to_json())
        return jsonify(message=str(message.id))

    def delete(self, conversation_id):
        pass


conversations_view = ConversationAPI.as_view('conversation_api')
conversations.add_url_rule(
    '/', defaults={'conversation_id': None}, view_func=conversations_view, methods=['GET', ])
conversations.add_url_rule(
    '/', view_func=conversations_view, methods=['POST', ])
conversations.add_url_rule('/<conversation_id>', view_func=conversations_view,
                           methods=['GET', 'PUT', 'DELETE'])
