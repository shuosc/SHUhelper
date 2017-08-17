from flask import Blueprint, request, jsonify
from .models import Course, CourseOfTerm
courses = Blueprint('courses', __name__)


@courses.route('/')
def get_courses():
    args = request.get_json()
    page = args['page']
    courses = Course.objects(
        no__contains=args['no'],
        name__contains=args['name'],
        teacher__contains=args['teacher'],
        credit__contains=args['credit']).paginate(page=page, per_page=30)
    return jsonify(courses.items())


@courses.route('/<oid>')
def get_course(oid):
    course = Course.objects.get_or_404(_id=oid)
    term_courses = CourseOfTerm.objects(course=course)
    return jsonify(course=course,terms=term_courses)

