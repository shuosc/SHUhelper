from flask import Blueprint, abort, jsonify, request, current_app
from flask_login import current_user, login_required
from mongoengine.queryset.visitor import Q

from .manage import get_xk, get_teachers
from .models import Course, CourseOfTerm, Teacher

courses = Blueprint('courses', __name__)


@courses.route('/manage/migrate')
@login_required
def migrate():
    if current_user.role != 'superadmin':
        abort(401)
    for course_of_term in CourseOfTerm.objects():
        course_of_term.course_no = course_of_term.course.no
        course_of_term.course_name = course_of_term.course.name
        course_of_term.teacher = course_of_term.course.teacher
        course_of_term.teacher_name = course_of_term.course.teacher.name
        course_of_term.credit = course_of_term.course.credit
        course_of_term.save()
    return jsonify(success='ok')


@courses.route('/manage/update-term')
@login_required
def update_term():
    term = current_app.school_time.term_string
    if current_user.role != 'superadmin':
        abort(401)
    for course in Course.objects():
        if CourseOfTerm.objects(course=course, term=term).get() is not None:
            course.this_term = True
        else:
            course.this_term = False
        course.save()
    return jsonify(status='ok')


@courses.route('/manage/update-teachers')
@login_required
def get_teachers_api():
    if current_user.role != 'superadmin':
        abort(401)
    get_teachers()
    return jsonify(success='ok')


@courses.route('/manage/update-course/80')
@login_required
def get_courses_80():
    if current_user.role != 'superadmin':
        abort(401)
    get_xk('http://xk.shu.edu.cn/')
    return jsonify(success='ok')


@courses.route('/manage/update-course/8080')
@login_required
def get_courses_8080():
    if current_user.role != 'superadmin':
        abort(401)
    get_xk('http://xk.shu.edu.cn:8080/')
    return jsonify(success='ok')


@courses.route('/')
def get_courses():
    args = request.args
    query_type = args.get('type')
    page = args['page']
    per_page = args.get('perPage', 30)
    if query_type == 'quick':
        query = args['query']
        this_term = args['thisTerm']
        courses = Course.objects(
            (
                Q(no__contains=query) |
                Q(name__contains=query) |
                Q(teacher__contains=query)
            ) &
            Q(this_term=this_term)
        ).paginate(page=int(page), per_page=30)
        return jsonify(courses.items)
    elif query_type == 'advance':
        courses = CourseOfTerm.objects(
            course_no__contains=args.get('no'), course_name__contains=args.get('name'),
            time__contains=args.get('time'), teacher_name__contains=args.get('teacher'),
            campus__contains=args.get('campus'), credit__contains=args.get('credit'),
            term=args.get('term')).no_dereference()
        return jsonify(total=courses.count(), courses=courses.paginate(page=int(page), per_page=per_page).items)
    else:
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
