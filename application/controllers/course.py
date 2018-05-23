from datetime import datetime
from functools import reduce

import requests
from flask import Blueprint, Flask, jsonify, request, current_app
from flask.views import MethodView
from flask_login import current_user, login_required

from application.extensions import db
from application.models.course import *
from application.utils import register_api
course = Blueprint('course', __name__)


class CourseAPI(MethodView):
    def get(self, course_id):
        if course_id is None:
            page = request.args.get('page', 1, int)
            per_page = request.args.get('perPage', 15, int)
            course_id = request.args.get('id', '')
            name = request.args.get('name', '')
            dept = request.args.get('dept', '')
            credit = request.args.get('credit', '')
            # search = request.args.get('search', '')
            courses = Course.query.filter(
                Course.id.contains(course_id) &
                Course.name.contains(name) &
                Course.dept.contains(dept) &
                Course.credit.contains(credit)
            ).order_by(Course.id)
            # courses = Course.query.all()
            paginated_courses = courses.paginate(
                page=page, per_page=per_page)
            # print(paginated_courses.items[0])
            result = courses_schema.dump(paginated_courses.items)
            return jsonify(courses=result.data, total=courses.count())
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
        course = Course.query.get(course_id)
        # course.id = json_post['id']
        course.name = json_post['name']
        course.credit = json_post['credit']
        course.detail = json_post['detail']
        course.dept = json_post['dept']
        course.save()
        return course_schema.jsonify(course)

    def delete(self, course_id):
        course = Course.query.get(course_id)
        course.delete()
        return jsonify(success=True)


register_api(course, CourseAPI, 'course_api', '/', pk='course_id')