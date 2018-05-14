"""
auth_views.py

    all of the routes related to user authorization and credentials

"""

from flask import flash, redirect, url_for, render_template_string
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import google
from flask_login import logout_user, login_required, login_user

from project import app
from project import google_blueprint
from project.auth.firebase_user import get_firebase_user_by_email, create_firebase_user, InvalidEmailAddress, CONVERTER_STRING
from project.views.view_utils import logout_required


@app.route('/log_out')
@login_required
def log_out() -> str:
    logout_user()
    return redirect(url_for('index'))

@app.route("/go_to_login")
@logout_required
def go_to_login():
    '''
    HACK for linking to google login
    :return:
    '''
    return render_template_string("<a href=\"{{ url_for('google.login') }}\">follow this link to login to SUICIDE CHESS >>></a>")

@oauth_authorized.connect_via(google_blueprint)
@logout_required
def log_in(blueprint, token):
    # get oauth response
    resp = google.get("/oauth2/v2/userinfo")
    email_id = resp.json()['email']

    if resp.ok:
        # see if the user already exists
        user = get_firebase_user_by_email(email_id)

        # if they don't exist create a new user
        if not user:
            try:
                display_name = resp.json()['name']
                user = create_firebase_user(display_name, email_id)
            except InvalidEmailAddress:
                flash("This email address is invalid. It cannot have % in it." % CONVERTER_STRING)
                redirect(url_for("index"))

        # login the user
        login_user(user)
