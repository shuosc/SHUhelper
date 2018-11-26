from functools import wraps
from flask import abort
from flask_login import current_user
from application.user.models import User


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            if not current_user.can(permission):
                abort(403)
            return decorated_function(*args,**kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required()(f)