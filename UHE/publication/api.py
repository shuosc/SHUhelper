from flask import Blueprint, jsonify, request, abort
from flask.views import MethodView
from flask_login import current_user

from UHE.publication.models import Publication
from UHE.plugins.SHU_course.models import Course

publications = Blueprint('publications', __name__)


# TYPE_DICT = {
#     'feed': Feed,
#     'course': Course
# }


class PublicationAPI(MethodView):
    def get(self, publication_id=None, page=1):
        publications = Publication.objects()
        return jsonify(publications)
        # post_type = request.args.get('post')
        # post_id = request.args.get('id')
        # if post_type is not None and post_id is not None:
        #     post = TYPE_DICT[post_type].objects(id=post_id).get_or_404()
        #     comments = Comment.objects(post=post)
        #     return jsonify([comment.to_dict() for comment in comments])
        # else:
        #     if not comment_id:
        #         paginated_comments = Comment.objects.paginate(
        #             page=page, per_page=20)
        #         return jsonify(paginated_comments.items)

    def post(self):
        pass
        # args = request.get_json()
        # post = TYPE_DICT[args['post']].objects(id=args['id']).first()
        # comment = Comment(user=current_user.to_dbref(), post=post,
        #                   content=args['content'])
        # comment.save()
        # post.comments.append(comment)
        # post.save()
        # return jsonify({'id': str(comment.id)})

    def put(self, feed_id):
        pass

    def delete(self, comment_id):
        pass
        # comment = Comment.objects(id=comment_id).get_or_404()
        # if comment.user.id == current_user.id:
        #     comment.delete()
        # else:
        #     abort(401)
        # return jsonify(status='ok')


publications_view = PublicationAPI.as_view('publication_api')
publications.add_url_rule(
    '/', defaults={'publication_id': None}, view_func=publications_view, methods=['GET', ])
publications.add_url_rule(
    '/', view_func=publications_view, methods=['POST', ])
publications.add_url_rule('/<publication_id>', view_func=publications_view,
                      methods=['GET', 'PUT', 'DELETE'])
