from flask import Blueprint, abort, jsonify, request
from flask_login import current_user, login_required
from mongoengine.queryset.visitor import Q

from .manage import get_xk, get_teachers
from .models import Course, CourseOfTerm,Teacher

teachers = Blueprint('teachers', __name__)
