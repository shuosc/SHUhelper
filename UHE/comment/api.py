from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import current_user
from bson import ObjectId
from UHE.comment.models import Comment
from UHE.feed.models import Feed
from UHE.plugins.SHU_course.models import Course
comments = Blueprint('comments', __name__)


@comments.route('/<comment_id>/like')
def like(comment_id):
    Comment.objects(id=comment_id).update_one(push__like=current_user.id)
    return jsonify(id=str(comment_id))


TYPE_DICT = {
    'feed': Feed,
    'course': Course
}


class CommentAPI(MethodView):
    def get(self, comment_id=None, page=1):
        post_type = request.args.get('post')
        post_id = request.args.get('id')
        if post_type is not None and post_id is not None:
            post = TYPE_DICT[post_type].objects(id=post_id).get_or_404()
            comments = Comment.objects(post=post)
            return jsonify([comment.to_dict() for comment in comments])
        else:
            if not comment_id:
                paginated_comments = Comment.objects.paginate(
                    page=page, per_page=20)
                return jsonify(paginated_comments.items)

    def post(self):
        args = request.get_json()
        post = TYPE_DICT[args['post']].objects(id=args['id']).first()
        comment = Comment(user=current_user.to_dbref(), post=post,
                          content=args['content'])
        comment.save()
        post.comments.append(comment)
        post.save()
        return jsonify({'id': str(comment.id)})

    def put(self, feed_id):
        pass


    def delete(self, comment_id):
        comment = Comment.objects(id=comment_id).get_or_404()
        if comment.user.id == current_user.id:
            comment.delete()
        else:
            abort(401)
        return jsonify(status='ok')


comments_view = CommentAPI.as_view('comment_api')
comments.add_url_rule(
    '/', defaults={'comment_id': None}, view_func=comments_view, methods=['GET', ])
comments.add_url_rule(
    '/', view_func=comments_view, methods=['POST', ])
comments.add_url_rule('/<comment_id>', view_func=comments_view,
                      methods=['GET', 'PUT', 'DELETE'])
