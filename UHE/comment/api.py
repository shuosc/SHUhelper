from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_login import current_user

from UHE.comment.models import Comment

comments = Blueprint('comments', __name__)


@comments.route('/<comment_id>/like')
def like(comment_id):
    Comment.objects(id=comment_id).update_one(push__liked=current_user.id)
    return jsonify(id=str(comment_id))


class CommentAPI(MethodView):
    def get(self, comment_id=None, page=1):
        if not comment_id:
            paginated_comments = Comment.objects.paginate(
                page=page, per_page=20)
            return jsonify([comment.to_dict() for comment in paginated_comments])
        else:
            comment = Comment.objects.get_or_404(id=comment_id)
            return comment(feed.to_dict())

    def post(self):
        args = request.get_json()
        feed = Feed(user=current_user.id,
                    feed_type=args['type'], text=args['type'], link=args['link'], img=args['img'])
        feed.save()
        return jsonify({'id': feed.id})

    def put(self, feed_id):
        feed = Feed.objects.get_or_404(id=feed_id)
        args = request.get_json()
        comments = Comment(user=current_user.id,
                           content=args['content'], message=pargrams['message'])
        message.save()
        conversation.messages.append(message)
        conversation.save()

    def delete(self, conversation_id):
        pass


comments_view = CommentAPI.as_view('conversation_api')
convcommentsersations.add_url_rule(
    '/', defaults={'comment_id': None}, view_func=comments_view, methods=['GET', ])
comments.add_url_rule(
    '/', view_func=comments_view, methods=['POST', ])
comments.add_url_rule('/<comment_id>', view_func=comments_view,
                      methods=['GET', 'PUT', 'DELETE'])
