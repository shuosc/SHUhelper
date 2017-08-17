from flask import Blueprint, jsonify, request
# from flask_login import current_user.
from flask.views import MethodView
from flask_login import current_user, login_required
from mongoengine.queryset.visitor import Q

from UHE.message.models import Conversation, Message
from UHE.user.models import User

conversations = Blueprint('conversations', __name__)


class ConversationAPI(MethodView):
    decorators = [login_required]

    def get(self, conversation_id=None):
        if not conversation_id:
            conversations = Conversation.objects(
                Q(to_user=current_user.id) | Q(from_user=current_user.id))
            return jsonify([conversation.to_dict_abstract() for conversation in conversations])
        else:
            conversation = Conversation.objects.get_or_404(id=conversation_id)
            return jsonify(conversation.to_dict_complete())

    def post(self):
        args = request.get_json()
        to_user = User.objects(card_id=args['to']).first()
        if to_user is None:
            to_user = User(card_id=args['to'])
            to_user.save()
        else:
            conversation = Conversation.objects(
                (Q(to_user=to_user.id, from_user=current_user.id) | (Q(to_user=current_user.id, from_user=to_user.id)))).first()
            if conversation is None:
                conversation = Conversation(
                    from_user=current_user.id, to_user=to_user, messages=[])
                conversation.save()
        return jsonify({'id': str(conversation.id)})

    def put(self, conversation_id):
        # conversation = Conversation.objects.get_or_404(id=conversation_id)
        args = request.get_json()
        print(args)
        message = Message(sender=current_user.id,
                          message_type="private", content=args['content'])
        message.save()
        Conversation.objects(id=conversation_id).update_one(
            push__messages=message)
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
