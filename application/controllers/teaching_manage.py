from datetime import datetime
from functools import reduce

import requests
from flask import Blueprint, Flask, current_app, jsonify, request
from flask.views import MethodView
from flask_login import current_user, login_required

from application.extensions import db
from application.models.teaching_manage import Class,StudentClass,Course,class_schema,classes_schema,course_schema,courses_schema
from application.models.teaching_manage import UndergraduateStudent as Student
from application.models.teaching_manage import \
    undergraduate_student_schema as student_schema
from application.models.teaching_manage import \
    undergraduate_students_schema as students_schema
from application.models.teaching_manage import Teacher, teacher_schema, teachers_schema
from application.models.user import User
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
            return jsonify(courses=result, total=courses.count())
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


register_api(course, CourseAPI, 'course_api',
             '/', pk='course_id', pk_type='str')


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
            return jsonify(teachers=result, total=teachers.count())
        else:
            teacher = Teacher.query.get(teacher_id)
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
        # teacher.credit = json_post['credit']
        # teacher.detail = json_post['detail']
        teacher.dept = json_post['dept']
        teacher.save()
        return teacher_schema.jsonify(teacher)

    def delete(self, teacher_id):
        teacher = Teacher.query.get(teacher_id)
        teacher.delete()
        return jsonify(success=True)


register_api(teachers, TeacherAPI, 'teacher_api',
             '/', pk='teacher_id', pk_type='str')


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
            return jsonify(students=result, total=students.count())
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
        # student.credit = j/son_post['credit']
        # student.detail = json_post['detail']
        student.dept = json_post['username']
        student.save()
        return student_schema.jsonify(student)

    def delete(self, student_id):
        student = Student.query.get(student_id)
        student.delete()
        return jsonify(success=True)


register_api(students, StudentAPI, 'student_api', '/', pk='student_id')

@students.route('/<student_id>/classes',methods=['GET','POST'])
def student_class(student_id):
    if request.method == 'GET':
        term = request.args.get('term')
        student = Student.query.get(student_id)
        classes = student.classes
        print(classes)
    else:
        term = request.args.get('term')
        json_post = request.json
        student = Student.query.get(student_id)
        classes = student.classes
        for _class in classes:
            pass

_class = Blueprint('_class', __name__)


class ClassAPI(MethodView):
    def get(self, class_id):
        if class_id is None:
            page = request.args.get('page', 1, int)
            per_page = request.args.get('perPage', 10, int)
            course_name = request.args.get('courseName', '')
            course_id = request.args.get('courseID', '')
            teacher_id = request.args.get('teacherID', '')
            teacher_name = request.args.get('teacherName', '')
            term = request.args.get('term', '')
            campus = request.args.get('campus', '')
            credit = request.args.get('credit', '')
            time = request.args.get('time', '')
            # search = request.args.get('search', '')
            print(teacher_name)
            classes = Class.query.filter(Class.course_id == Course.id)\
                .filter(Course.name.contains(course_name), Course.credit.contains(credit))\
                .filter(Class.teacher_id == User.id)\
                .filter(User.name.contains(teacher_name), User.id.startswith(teacher_id))\
                .filter(
                    Class.time.contains(time),
                    Class.course_id.contains(course_id),
                    # Class.teacher_id.startswith(teacher_id) &
                    Class.term.contains(term),
                    Class.campus.contains(campus))
            paginated_classes = classes.paginate(
                page=page, per_page=per_page)
            result = classes_schema.dump(paginated_classes.items)
            return jsonify(classes=result, total=classes.count())
        else:
            _class = Course.query.filter.get(course_id)
            return class_schema.jsonify(_class)

    def post(self):
        json_post = request.json
        _class = class_schema.load(json_post)
        print(_class.class_id)
        _class.save()
        # return _class.jsonify(_class)
        return class_schema.jsonify(_class)

    def put(self, class_id):
        json_post = request.json
        _class = Class.query.get(class_id)
        # course.id = json_post['id']
        _class.teacher_id = json_post['teacherID']
        _class.capacity = json_post['capacity']
        _class.campus = json_post['campus']
        _class.time = json_post['time']
        _class.term = json_post['term']
        _class.classroom = json_post['classroom']
        _class.save()
        return class_schema.jsonify(_class)

    def delete(self, class_id):
        _class = Class.query.get(class_id)
        _class.delete()
        return jsonify(success=True)


register_api(_class, ClassAPI, '_class_api', '/', pk='class_id')

select = Blueprint('select', __name__)


class SelectAPI(MethodView):
    def get(self, class_id):
        if class_id is None:
            page = request.args.get('page', 1, int)
            per_page = request.args.get('perPage', 15, int)
            course_name = request.args.get('courseName', '')
            course_id = request.args.get('courseID', '')
            teacher_id = request.args.get('teacherID', '')
            term = request.args.get('term', '')
            campus = request.args.get('campus', '')
            # search = request.args.get('search', '')
            classes = Class.query.filter(Class.course_id == Course.id).filter(
                Course.name.contains(course_name) &
                Class.course_id.contains(course_id) &
                Class.teacher_id.startswith(teacher_id) &
                Class.term.contains(term) &
                Class.campus.contains(campus)
            ).order_by(Class.course_id)
            # courses = Course.query.all()
            paginated_classes = classes.paginate(
                page=page, per_page=per_page)
            # print(paginated_courses.items[0])
            result = classes_schema.dump(paginated_classes.items)
            return jsonify(classes=result, total=classes.count())
        else:
            _class = Course.query.filter.get(course_id)
            return class_schema.jsonify(_class)

    def post(self):
        json_post = request.json
        _class = class_schema.load(json_post)
        print(_class.class_id)
        _class.save()
        # return _class.jsonify(_class)
        return class_schema.jsonify(_class)

    def put(self, class_id):
        json_post = request.json
        _class = Class.query.get(class_id)
        # course.id = json_post['id']
        _class.teacher_id = json_post['teacherID']
        _class.capacity = json_post['capacity']
        _class.campus = json_post['campus']
        _class.time = json_post['time']
        _class.term = json_post['term']
        _class.classroom = json_post['classroom']
        _class.save()
        return class_schema.jsonify(_class)

    def delete(self, class_id):
        _class = Class.query.get(class_id)
        _class.delete()
        return jsonify(success=True)


register_api(select, SelectAPI, 'select_api', '/', pk='id')


grades = Blueprint('grades', __name__)
