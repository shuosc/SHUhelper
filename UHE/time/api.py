from flask import Blueprint, jsonify
from . import Time
time = Blueprint('time', __name__)


@time.route('/')
def index():
    time_tuple = Time().time_tuple()
    return jsonify(year=time_tuple[0], term=time_tuple[1], week=6, day=time_tuple[3], course=time_tuple[4])
