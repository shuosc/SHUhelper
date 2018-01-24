from flask import Blueprint, abort, jsonify, request, current_app
from flask_login import current_user, login_required
from mongoengine.queryset.visitor import Q

from .manage import get_xk, get_teachers
from .models import Course, CourseOfTerm, Teacher, Evaluation

courses = Blueprint('courses', __name__)


@courses.route('/manage/migrate')
@login_required
def migrate():
    if current_user.role != 'superadmin':
        abort(401)
    i = 0
    for course in Course.objects():
        i += 1
        print(i)
        course_of_term = CourseOfTerm.objects(course=course)
        new_course = Course(
            no=course.no,
            name=course.name,
            teacher=course.teacher,
            teacher_name=course.teacher_name,
            credit=course.credit,
            school=course.school,
            terms=course.terms,
            liked=[],
            evaluations=[],
            tags=[]
        )
        course.no = course.no + '0'
        course.save()
        new_course.save()
        course_of_term.update(course=new_course)
        course.delete()
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
    page = int(args['page'])
    per_page = int(args.get('perPage', 10))
    if query_type == 'quick':
        query = args['query']
        # this_term = args['thisTerm']
        courses = Course.objects(
            (
                Q(no__contains=query) |
                Q(name__contains=query) |
                Q(teacher_name__contains=query)
            )
        )[per_page * (page - 1):per_page * page]
        return jsonify(
            total=courses.count(),
            courses=courses)
    elif query_type == 'advance':
        per_page = 30
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



@courses.route('/<oid>/like')
def like(oid):
    course = Course.objects(id=oid).get_or_404()
    if current_user.is_anonymous:
        user = User.objects(card_id="00000001").first()
        Course.objects(id=oid).update_one(push__like=user.to_dbref())
        course.heat += 1
    elif Course.objects(id=oid, like__nin=[current_user.to_dbref()]).first() is not None:
        Course.objects(id=oid).update_one(push__like=current_user.to_dbref())
        course.heat += 1
    else:
        course.heat -= 1
        Course.objects(id=oid).update_one(pull__like=current_user.to_dbref())
    course.save()
    course.reload()
    return jsonify(course)

@courses.route('/<oid>', methods=['GET', 'PUT'])
def get_course(oid):
    if request.method == 'GET':
        course = Course.objects.get_or_404(id=oid)
        course.heat += 1
        course.save()
        # term_courses = CourseOfTerm.objects(course=course)
        # for evaluation in course.evaluations:
        #     evaluation.user = evaluation.user.to_dict_public()
        return jsonify(course=course)

# @course.route('/')
# def get_course_id():


@courses.route('/<oid>/<term>')
def get_course_by_term(oid, term):
    course = Course.objects.get_or_404(id=oid)
    term_courses = CourseOfTerm.objects(course=course, term=term)
    return jsonify(course=course, classes=term_courses)
