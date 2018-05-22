from datetime import datetime
from functools import reduce

import requests
from flask import Blueprint, Flask, jsonify, request, current_app
from flask.views import MethodView
from flask_login import current_user, login_required

from application.extensions import db
from application.models.teaching_manage import *

course = Blueprint('course', __name__)


class CourseAPI(MethodView):
    def get(self, course_id):
        if course_id is None:
            if search:
                courses = Course


class ClassAPI(MethodView):
    pass


class StudentCourseAPI(MethodView):
    pass


class LostNFoundAPI(MethodView):
    decorators = [login_required]

    def get(self, post_id):
        if post_id is None:
            posts_type = request.args.get('type', 'found')
            author_id = request.args.get('authorID')
            page = request.args.get('page', 1, int)
            search = request.args.get('search', False)
            if search:
                posts = Post.query.filter((Post.title.contains(search) |
                                           Post.site.contains(search) |
                                           Post.category.contains(search) |
                                           Post.content.contains(search) |
                                           Post.address.contains(search)) &
                                          Post.type.contains(posts_type))
            else:
                if author_id is None:
                    posts = Post.query.filter_by(type=posts_type)
                else:
                    posts = Post.query.filter_by(author_id=author_id)
            posts = posts.order_by(Post.lighten_time.desc())
            paginated_posts = posts.paginate(page=page, per_page=15)
            return jsonify(posts=[post.to_json() for post in paginated_posts.items])
        else:
            post = Post.query.filter_by(id=post_id).first()
            return jsonify(post=post.to_json())

    def post(self):
        json_post = request.json
        json_post['authorID'] = current_user.id
        post = Post.from_json(json_post)
        post.save()
        return jsonify(post=post.to_json())

    def delete(self, post_id):
        if post_id is None:
            return jsonify(msg="无权限"), 401
        else:
            post = Post.query.filter_by(id=post_id).first()
            if not post.user_id == current_user.id:
                return jsonify(msg="无权限"), 401
            post.delete()
            return jsonify(success=True)

    def put(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        if not post.user_id == current_user.id:
            return jsonify(msg="无权限"), 401
        json_post = request.json
        is_founded = json_post['isFounded']
        post.change_found_status(is_founded)
        return jsonify(post=post.to_json())


view = LostNFoundAPI.as_view('lost_n_found_api')
lost_n_found.add_url_rule('/', defaults={'post_id': None},
                          view_func=view, methods=['GET', ])
lost_n_found.add_url_rule('/', view_func=view, methods=['POST', ])
lost_n_found.add_url_rule('/<post_id>', view_func=view,
                          methods=['GET', 'PUT', 'DELETE'])
