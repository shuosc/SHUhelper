from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import current_user
from bson import ObjectId
from UHE.comment.models import Comment

comments = Blueprint('comments', __name__)


@comments.route('/<comment_id>/like')
def like(comment_id):
    Comment.objects(id=comment_id).update_one(push__like=current_user.id)
    return jsonify(id=str(comment_id))


class CommentAPI(MethodView):
    def get(self, post_id=None, page=1):
        if not post_id:
            paginated_comments = Comment.objects.paginate(
                page=page, per_page=20)
            return jsonify(paginated_comments.items)
        else:
            comments = Comment.objects.get_or_404(post=ObjectId(post_id))
            return jsonify(comments.items)

    def post(self):
        args = request.get_json()
        comment = Comment(user=current_user.id,
                          display_name=args['name'], content=args['content'])
        comment.save()
        return jsonify({'id': comment.id})

    def put(self, feed_id):
        pass
        # feed = Feed.objects.get_or_404(id=feed_id)
        # args = request.get_json()
        # comments = Comment(user=current_user.id,
        #                    content=args['content'], message=pargrams['message'])
        # message.save()
        # conversation.messages.append(message)
        # conversation.save()

    def delete(self, conversation_id):
        pass


comments_view = CommentAPI.as_view('comment_api')
comments.add_url_rule(
    '/', defaults={'comment_id': None}, view_func=comments_view, methods=['GET', ])
comments.add_url_rule(
    '/', view_func=comments_view, methods=['POST', ])
comments.add_url_rule('/<comment_id>', view_func=comments_view,
                      methods=['GET', 'PUT', 'DELETE'])
