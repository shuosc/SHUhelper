from flask import Blueprint, request, jsonify
from .models import Course, CourseOfTerm
from mongoengine.queryset.visitor import Q
courses = Blueprint('courses', __name__)


@courses.route('/')
def get_courses():
    args = request.args
    # print(args)
    # print(args)
    if args.get('quick'):
        page = args['page']
        query = args['query']
        courses = Course.objects(
            Q(no__contains=query) |
            Q(name__contains=query) |
            Q(teacher__contains=query)).paginate(page=int(page), per_page=30)
        return jsonify(courses.items)
    elif args.get('id'):
        print(args)
        course = Course.objects(
            Q(no__contains=args.get('no')) &
            Q(teacher__contains=args.get('teacher'))).get_or_404()
        return jsonify(id=str(course.id))
    else:
        page = args['page']
        courses = Course.objects(
            no__contains=args['no'],
            name__contains=args['name'],
            teacher__contains=args['teacher'],
            credit__contains=args['credit']).paginate(page=int(page), per_page=60)
        return jsonify(courses.items)


@courses.route('/<oid>')
def get_course(oid):
    course = Course.objects.get_or_404(id=oid)
    term_courses = CourseOfTerm.objects(course=course)
    return jsonify(course=course, terms=list(set(term_course.term for term_course in term_courses)))

# @course.route('/')
# def get_course_id():


@courses.route('/<oid>/<term>')
def get_course_by_term(oid, term):
    course = Course.objects.get_or_404(id=oid)
    term_courses = CourseOfTerm.objects(course=course, term=term)
    return jsonify(course=course, classes=term_courses)
