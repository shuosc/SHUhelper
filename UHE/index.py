import datetime

from flask import Blueprint, request, jsonify, current_app, abort, redirect, url_for, flash
from flask_login import login_user, logout_user

from UHE.client import Services
from UHE.email import send_async_email
from UHE.extensions import captcha_solver, redis_store
from UHE.user.models import User
from UHE.utils import make_token,validate
from UHE.plugins.SHU_course import get_term
index = Blueprint('index', __name__)
