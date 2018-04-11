from project import app
from project.forms.forms import LoginForm, SignupForm, verify_signup_form
from project.users.firebase_login import sign_in_firebase_user\
                        , create_firebase_user\
                        , delete_current_firebase_user\
                        , sign_out_firebase_user

from project.users.firebase_auth_errors import error_map, get_firebase_error_message
from project.models.new_user_data import new_user_data

from flask import render_template, flash, redirect, url_for, Markup
from flask_login import login_required, login_user, current_user


import requests
from functools import wraps

GETPOST = ['GET', 'POST']


### context processors ###
@app.context_processor
def inject_debug():
    return dict(debug=app.debug)

# decorators
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


### HOME PAGE ###
@app.route('/')
@app.route('/index')
def index() -> str:
    return render_template("index.html")


### ERROR HANDLING ###
@app.errorhandler(404)
def not_found_error(error):
    return "page not found 404 error: %s" % error, 404


@app.errorhandler(500)
def internal_error(error):
    return "internal server 500 error: %s" % error, 500


### USER CREATION AND AUTHENTICATION ###
@app.route('/log_out')
@login_required
def log_out() -> str:
    sign_out_firebase_user()
    return redirect(url_for('index'))


@app.route('/delete_account')
@login_required
def delete_account() -> str:
    delete_current_firebase_user()
    flash("your account has been deleted.")
    return redirect(url_for('index'))

def bulletize_messages(messages: list):
    bulleted_messages = ["<li>%s</li>" % m for m in messages]
    return "<ul>%s</ul>" % '\n'.join(bulleted_messages)

def title_and_messages(title: str, messages: list):
    return Markup("<h2>%s</h2><br/>%s" % (title, bulletize_messages(messages)))

@app.route('/sign_up', methods=GETPOST)
@logout_required
def sign_up() -> str:

    # display a form for user input
    signupform = SignupForm()

    # validate the form
    if signupform.validate_on_submit():
        # if the user has not properly confirmed their password
        signup_form_errors = verify_signup_form(signupform)
        if signup_form_errors:
            flash(title_and_messages("Sign Up Error", signup_form_errors))
            return redirect(url_for('sign_up'))

        # else make a new user with the provided input from the form

        # put all the user data into this dict
        user_data = new_user_data(display_name=signupform.display_name.data, e_mail=signupform.email.data)

        try:
            create_firebase_user(
                  signupform.email.data
                , signupform.password.data
                , **user_data
            )

            user = sign_in_firebase_user(signupform.email.data, signupform.password.data)
            login_user(user, remember=signupform.remember.data)

            # send an email verification
            current_user.send_email_verification()

            # flash back to the home page
            flash("Thank you for registering! Please go to your email and verify your account.")
            redirect(url_for('index'))


        except requests.exceptions.HTTPError as e:
            error_response = get_firebase_error_message(e)
            flash("Sign Up Error: %s" % error_map(error_response))
            return redirect(url_for("sign_up"))

    return render_template('signup.html', form=signupform)


@app.route('/log_in', methods=GETPOST)
@logout_required
def log_in() -> str:
    loginform = LoginForm()
    if loginform.validate_on_submit():
        # get the user
        try:
            user = sign_in_firebase_user(loginform.email.data, loginform.password.data)
            login_user(user, remember=loginform.remember.data)
            # flash back to the home page
            flash('welcome %s! you have logged in successfully' % current_user.get_db_property("displayName"))
            return redirect(url_for('index'))


        except requests.exceptions.HTTPError as e:
            error_response = get_firebase_error_message(e)
            flash("Log In Error: %s" % error_map(error_response))
            return redirect(url_for("log_in"))

    return render_template('login.html', form=loginform)


@app.route('/resend_email_verification', methods=GETPOST)
@login_required
def resend_email_verification():
    if current_user.get_auth_property("emailVerified"):
        flash("you have already verified your email!")
        return redirect(url_for("index"))

    current_user.send_email_verification()
    flash("email verification resent!")
    return redirect(url_for("index"))


### GAME ROOMS ###

@app.route('/play_random')
@login_required
@email_verified
def play_random() -> str:
    return 'play random'


@app.route('/play_friend')
@login_required
@email_verified
def play_friend() -> str:
    return 'play friend'
