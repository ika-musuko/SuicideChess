'''
view_utils.py

    functions to help with views, to be used across the view pages

'''

from functools import wraps

from flask import flash, url_for
from flask_login import current_user
from markupsafe import Markup
from werkzeug.utils import redirect

from project import app, room_manager

# use this to inject global variables into the template manager
@app.context_processor
def inject_app_context():
    return {
         "debug" : app.debug
        ,"room_manager" : room_manager
    }


# use a @logout_required decorator to require a user to be logged out to view
def logout_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            flash("you are already logged in")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_view


# output a list of messages into a buileted list
def bulletize_messages(messages: list):
    bulleted_messages = ["<li>%s</li>" % m for m in messages]
    return "<ul>%s</ul>" % '\n'.join(bulleted_messages)

# output a title and bulleted messages
def title_and_messages(title: str, messages: list):
    return Markup("<h2>%s</h2><br/>%s" % (title, bulletize_messages(messages)))


GETPOST = ['GET', 'POST']