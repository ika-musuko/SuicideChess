from functools import wraps

from flask import flash, url_for
from flask_login import current_user
from markupsafe import Markup
from werkzeug.utils import redirect

from project import app

@app.context_processor
def inject_debug():
    return dict(debug=app.debug)

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


def bulletize_messages(messages: list):
    bulleted_messages = ["<li>%s</li>" % m for m in messages]
    return "<ul>%s</ul>" % '\n'.join(bulleted_messages)


def title_and_messages(title: str, messages: list):
    return Markup("<h2>%s</h2><br/>%s" % (title, bulletize_messages(messages)))