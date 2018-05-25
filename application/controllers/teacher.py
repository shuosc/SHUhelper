from datetime import datetime
from functools import reduce

import requests
from flask import Blueprint, Flask, jsonify, request, current_app
from flask.views import MethodView
from flask_login import current_user, login_required

from application.utils import register_api
from application.extensions import db
from application.models.user import Teacher, teacher_schema, teachers_schema

teachers = Blueprint('teacher', __name__)


class TeacherAPI(MethodView):
    def get(self, teacher_id):
        if teacher_id is None:
            page = request.args.get('page', 1, int)
            per_page = request.args.get('perPage', 15, int)
            teacher_id = request.args.get('id', '')
            name = request.args.get('name', '')
            teachers = Teacher.query.filter(
                Teacher.id.contains(teacher_id) &
                Teacher.name.contains(name)).order_by(Teacher.id)
            paginated_teachers = teachers.paginate(
                page=page, per_page=per_page)
            # print(paginated_teachers.items[0])
            result = teachers_schema.dump(paginated_teachers.items)
            return jsonify(teachers=result.data, total=teachers.count())
        else:
            teacher = Teacher.get(teacher_id)
            return teacher_schema.jsonify(teacher)

    def post(self):
        json_post = request.json
        teacher = teacher_schema.load(json_post)
        teacher.save()
        return teacher_schema.jsonify(teacher)

    def put(self, teacher_id):
        json_post = request.json
        teacher = Teacher.query.get(teacher_id)
        # teacher.id = json_post['id']
        teacher.name = json_post['name']
        teacher.credit = json_post['credit']
        teacher.detail = json_post['detail']
        teacher.dept = json_post['dept']
        teacher.save()
        return teacher_schema.jsonify(teacher)

    def delete(self, teacher_id):
        teacher = Teacher.query.get(teacher_id)
        teacher.delete()
        return jsonify(success=True)


register_api(teachers, TeacherAPI, 'teacher_api', '/', pk='teacher_id')
