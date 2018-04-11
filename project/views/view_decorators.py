from functools import wraps

from flask import flash, url_for
from flask_login import current_user
from werkzeug.utils import redirect


def logout_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            flash("you are already logged in")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_view


def email_verified(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if not (current_user.is_authenticated or current_user.get_auth_property("emailVerified")):
            return "you must verify your email to view this content", 401
        return f(*args, **kwargs)
    return decorated_view