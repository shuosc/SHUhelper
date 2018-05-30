from datetime import datetime
from functools import reduce

import requests
from flask import Blueprint, Flask, current_app, jsonify, request
from flask.views import MethodView
from flask_login import current_user, login_required

from application.extensions import db
from application.models.teaching_manage import Class, StudentClass, Course, class_schema, classes_schema, course_schema, courses_schema, student_class_schema, student_classes_schema
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


@teachers.route('/<teacher_id>/classes', methods=['GET', 'POST'])
def teacher_class(teacher_id):
    if request.method == 'GET':
        term = request.args.get('term')
        classes = Class.query.filter(
            Class.teacher_id == Teacher.id, Teacher.id == teacher_id).filter(Class.term == term)
        # classes = student.classes
        # print(classes)
        result = classes_schema.dump(classes.all())
        return jsonify(classes=result, total=classes.count())
    else:
        # term = request.args.get('term')
        class_ids = request.json['courses']
        # print(class_ids)
        student = Student.query.get(student_id)
        for _class in student.classes:
            class_id = str(_class.class_id)
            if class_id not in class_ids:
                student_class = StudentClass.query.filter_by(
                    student_id=student_id, class_id=class_id).first()
                # print('deleteing', student_class)
                student_class.delete()
        for class_id in class_ids:
            student_class = StudentClass.query.filter_by(
                student_id=student_id, class_id=class_id).first()
            if student_class is None:
                _class = Class.query.get(class_id)
                student_class = StudentClass()
                student_class.student = student
                student_class._class = _class
                # _class.students.append(student_class)
                # print('adding', student_class)
                student_class.save()
                # student.save()
        return jsonify(success=True)


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
            student = Student.query.get(student_id)
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


def grade_to_point(grade):
    if grade >= 90:
        return 4
    elif grade >= 85:
        return 3.7
    elif grade >= 82:
        return 3.3
    elif grade >= 78:
        return 3.0
    elif grade >= 75:
        return 2.7
    elif grade >= 72:
        return 2.3
    elif grade >= 68:
        return 2.0
    elif grade >= 66:
        return 1.7
    elif grade >= 64:
        return 1.5
    elif grade >= 60:
        return 1.0
    else:
        return 0


@students.route('/<student_id>/classes/<class_id>', methods=['PUT'])
def edit_student_class(student_id, class_id):
    student_class = StudentClass.query.filter_by(
        student_id=student_id, class_id=class_id).first()
    student_class.grade_1 = int(request.json['grade_1'])
    student_class.grade_2 = int(request.json['grade_2'])
    student_class.grade = student_class.grade_1 * 0.4 + student_class.grade_2 * 0.6
    student_class.point = grade_to_point(student_class.grade)
    student_class.save()
    return jsonify(student_class_schema.dump(student_class))


@students.route('/<student_id>/trends', methods=['GET'])
def student_trends(student_id):
    student_classes = StudentClass.query.filter_by(
        student_id=student_id)
    average = {}
    for s_class in student_classes:
        if average.get(s_class._class.term) is None:
            average[s_class._class.term] = [0, 0]
        if s_class.point is not None:
            average[s_class._class.term][0] += s_class.point * \
                float(s_class._class.course.credit)
            average[s_class._class.term][1] += float(
                s_class._class.course.credit)
    for term in average:
        average[term] = average[term][0]/average[term][1]
    return jsonify(terms=sorted(average.keys()), points=[average[k] for k in sorted(average.keys())])


@students.route('/<student_id>/classes', methods=['GET', 'POST'])
def student_class(student_id):
    if request.method == 'GET':
        term = request.args.get('term')
        if term:
            student_classes = StudentClass.query.filter(
                StudentClass.student_id == student_id, StudentClass.class_id == Class.id).filter(Class.term == term)
        else:
            student_classes = StudentClass.query.filter(
                StudentClass.student_id == student_id, StudentClass.class_id == Class.id)
        grade_sum = 0
        credit_sum = 0
        for student_class in student_classes:
            if student_class.point is not None:
                credit = float(student_class._class.course.credit)
                grade_sum += student_class.point * credit
                credit_sum += credit
        result = student_classes_schema.dump(student_classes.all())
        if credit_sum == 0:
            gpa = 0
        else:
            gpa = grade_sum/credit_sum
        return jsonify(gpa=gpa, classes=result, total=student_classes.count())
    else:
        term = request.args.get('term')
        class_ids = request.json['courses']
        # print(class_ids)
        student = Student.query.get(student_id)
        for _class in student.classes:
            class_id = str(_class.class_id)
            if class_id not in class_ids:
                student_class = StudentClass.query.filter_by(
                    student_id=student_id, class_id=class_id).first()
                # print('deleteing', student_class)
                if student_class.term == term:
                    student_class.delete()
        for class_id in class_ids:
            student_class = StudentClass.query.filter_by(
                student_id=student_id, class_id=class_id).first()
            if student_class is None:
                _class = Class.query.get(class_id)
                student_class = StudentClass()
                student_class.student = student
                student_class._class = _class
                # _class.students.append(student_class)
                # print('adding', student_class)
                student_class.save()
                # student.save()
        return jsonify(success=True)


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
            # print(teacher_name)
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
        # print(_class.class_id)
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


@_class.route('/<class_id>/stat')
def class_stat():
    value = [0, 0, 0, 0, 0]
    student_classes = StudentClass.query.filter(class_id=class_id)
    for student_class in student_classes:
        if student_class.point is not None:
            point = student_class.point
            if point >= 3.7:
                value[0] += 1
            elif point >= 3.3:
                value[1] += 1
            elif point >= 3.0:
                value[2] += 1
            elif point >= 2.0:
                value[3] += 1
            elif point[4] >= 1.0:
                value[4] += 1
    return jsonify(value=value)


register_api(_class, ClassAPI, '_class_api', '/', pk='class_id')

student_class_bp = Blueprint('student_class', __name__)


class StudentClassAPI(MethodView):
    def get(self, id):
        page = request.args.get('page', 1, int)
        per_page = request.args.get('perPage', 15, int)
        course_name = request.args.get('courseName', '')
        course_id = request.args.get('courseID', '')
        teacher_id = request.args.get('teacherID', '')
        student_id = request.args.get('studentID', '')
        term = request.args.get('term', '')
        campus = request.args.get('campus', '')
        classes = StudentClass.query.filter(Class.course_id == Course.id, StudentClass.class_id == Class.id).filter(
            Course.name.contains(course_name),
            Class.course_id.contains(course_id),
            Class.teacher_id.startswith(teacher_id),
            StudentClass.student_id.startswith(student_id),
            Class.term.contains(term),
            Class.campus.contains(campus)
        )
        # courses = Course.query.all()
        paginated_classes = classes.paginate(
            page=page, per_page=per_page)
        # print(paginated_courses.items[0])
        result = student_classes_schema.dump(paginated_classes.items)
        return jsonify(classes=result, total=classes.count())

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


register_api(student_class_bp, StudentClassAPI,
             'student_class_api', '/', pk='id')


grades = Blueprint('grades', __name__)
