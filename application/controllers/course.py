from datetime import datetime
from functools import reduce

import requests
from flask import Blueprint, Flask, jsonify, request, current_app
from flask.views import MethodView
from flask_login import current_user, login_required

from application.extensions import db
from application.models.course import *

course = Blueprint('course', __name__)


class CourseAPI(MethodView):
    def get(self, course_id):
        if course_id is None:
            page = request.args.get('page', 1, int)
            per_page = request.args.get('perPage', 15, int)
            search = request.args.get('search', False)
            if search:
                courses = Course.query.filter(
                    Course.id.contains(search) |
                    Course.name.contains(search)
                )
            else:
                courses = Course.query.all()
                paginated_courses = courses.paginate(
                    page=page, per_page=per_page)
                return courses_schema.jsonify(paginated_courses.items)
        else:
            course = Course.get(course_id)
            return course_schema.jsonify(course)

    def post(self):
        json_post = request.json
        course = course_schema.load(json_post)
        course.save()
        return course_schema.jsonify(course)

    def put(self, course_id):
        json_post = request.json
        course = Course.get(course_id)
        course.id = json_post['id']
        course.name = json_post['name']
        course.credit = json_post['credit']
        course.save()
        return course_schema.jsonify(course)

    def delete(self, course_id):
        course = Course.get(course_id)
        course.delete()
        return jsonify(success=True)


view = CourseAPI.as_view('course_api')
course.add_url_rule('/', defaults={'course_id': None},
                    view_func=view, methods=['GET', ])
course.add_url_rule('/', view_func=view, methods=['POST', ])
course.add_url_rule('/<course_id>', view_func=view,
                    methods=['GET', 'PUT', 'DELETE'])
