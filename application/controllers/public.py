from flask import Blueprint, jsonify, request, current_app
from qiniu import Auth
from flask_login import login_required,current_user

public = Blueprint('public', __name__)

@public.route('/sports-schedule/<term>')
def get_sports_schedule(term):
    pass

@public.route('/empty-room')
def get_empty_room():
    pass

@public.route('/time')
def get_school_time():
    pass

@public.route('/regulations')
def get_regulations():
    pass

@public.route('/sites-navigation')
def get_site_navigation():
    pass

@public.route('/school-bus')
def get_school_bus_schedule():
    pass

@public.route('/calendar')
def get_calendar():
    pass
