from flask import Blueprint, jsonify, request
from mongoengine.queryset.visitor import Q

from .models import Teacher

teachers = Blueprint('teachers', __name__)

@teachers.route('/')
def get_teachers():
    args = request.args
    page = args['page']
    query = args['query']
    teachers = Teacher.objects(
        Q(no__contains=query) |
        Q(name__contains=query)).paginate(page=int(page), per_page=30)
    return jsonify(teachers.items)


@teachers.route('/<oid>')
def get_teacher(oid):
    teacher = Teacher.objects.get_or_404(no=oid)
    return jsonify(name=teacher.name,no=teacher.no)
