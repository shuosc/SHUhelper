from datetime import datetime
from functools import reduce

import requests
from flask import Blueprint, Flask, jsonify, request, current_app
from flask.views import MethodView
from flask_login import current_user, login_required

from application.utils import register_api
from application.extensions import db
from application.models.user import UndergraduateStudent as Student, undergraduate_student_schema as student_schema, undergraduate_students_schema as students_schema

students = Blueprint('student', __name__)


class StudentAPI(MethodView):
    def get(self, student_id):
        if student_id is None:
            page = request.args.get('page', 1, int)
            per_page = request.args.get('perPage', 15, int)
            student_id = request.args.get('id', '')
            name = request.args.get('name', '')
            students = Student.query.filter(
                Student.id.contains(student_id) &
                Student.name.contains(name)).order_by(Student.id)
            paginated_students = students.paginate(
                page=page, per_page=per_page)
            # print(paginated_students.items[0])
            result = students_schema.dump(paginated_students.items)
            return jsonify(students=result.data, total=students.count())
        else:
            student = Student.get(student_id)
            return student_schema.jsonify(student)

    def post(self):
        json_post = request.json
        student = student_schema.load(json_post)
        student.save()
        return student_schema.jsonify(student)

    def put(self, student_id):
        json_post = request.json
        student = Student.query.get(student_id)
        # student.id = json_post['id']
        student.name = json_post['name']
        student.credit = json_post['credit']
        student.detail = json_post['detail']
        student.dept = json_post['dept']
        student.save()
        return student_schema.jsonify(student)

    def delete(self, student_id):
        student = Student.query.get(student_id)
        student.delete()
        return jsonify(success=True)


register_api(students, StudentAPI, 'student_api', '/', pk='student_id')