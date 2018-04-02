# -*- coding: utf-8 -*-
"""
    UHE.auth.api
    ~~~~~~~~~~~~~~~~~~
    
"""
from flask import Blueprint, jsonify, g,request,abort
from UHE.extensions import limiter
from datetime import datetime
from UHE.user.models import User
from flask_login import login_required
auth = Blueprint("auth", __name__)


@auth.before_request
def check_rate_limiting():
    """Check the the rate limits for each request for this blueprint."""
    return limiter.check()


@auth.errorhandler(429)
def login_rate_limit_error(error):
    """Register a custom error handler for a 'Too Many Requests'
    (HTTP CODE 429) error."""
    return jsonify(message='Too Many Requests')


def login_rate_limit():
    """Dynamically load the rate limiting config from the database."""
    # [count] [per|/] [n (optional)] [second|minute|hour|day|month|year]
    return "50/30minutes"


def login_rate_limit_message():
    """Display the amount of time left until the user can access the requested
    resource again."""
    current_limit = getattr(g, 'view_rate_limit', None)
    if current_limit is not None:
        window_stats = limiter.limiter.get_window_stats(*current_limit)
        reset_time = datetime.utcfromtimestamp(window_stats[0])
        timeout = reset_time - datetime.utcnow()
    return "{timeout}".format(timeout=timeout)


# Activate rate limiting on the whole blueprint
limiter.limit(login_rate_limit, error_message=login_rate_limit_message)(auth)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    """ main user auth view function
    user was authenticated when user has valid token (which stored in redis),
    or has valid cardID and password
    """
    if request.method == 'GET':
        token = request.args.get('token')
        user = User.verify_auth_token(token)
        if user is None:
            abort(401)
    else:
        json_post = request.get_json()
        user = User.query.get(json_post['id'])
        need_fresh = False
        if user is not None:
            need_fresh = not user.authenticate(json_post['password'])
        else:
            user = User(id=json_post['id'])
            need_fresh = True
        if need_fresh and not user.regisiter(json_post['password']):
            abort(403)
        token = user.generate_auth_token(864000)
    result = user.login(token)
    return jsonify(result)
