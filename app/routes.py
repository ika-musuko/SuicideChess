from app import app, pyre_auth, pyre_db
from .forms import LoginForm, SignupForm
from .firebase_login import sign_in_firebase_user\
                        , create_firebase_user\
                        , delete_current_firebase_user\
                        , current_user_db\
                        , current_user_auth

from .utils import get_firebase_error_message
from .error_maps import error_map

from flask import render_template, flash, redirect, url_for

import requests
from functools import wraps

GETPOST = ['GET', 'POST']


### decorators ###
def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if not pyre_auth.current_user:
            return "you must be logged in to view this content", 401
        return f(*args, **kwargs)
    return decorated_view

def logout_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if pyre_auth.current_user:
            flash("you are already logged in")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_view

def email_verified(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if not (pyre_auth.current_user or current_user_auth.get_property("emailVerified")):
            return "you must verify your email to view this content", 401
        return f(*args, **kwargs)
    return decorated_view

### HOME PAGE ###
@app.route('/')
@app.route('/index')
def index() -> str:
    return render_template("index.html", current_user_auth=current_user_auth, pyre_auth=pyre_auth, current_user_db=current_user_db)


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
    logout_user()
    return redirect(url_for('index'))


@app.route('/delete_account')
@login_required
def delete_account() -> str:
    delete_current_firebase_user()
    flash("your account has been deleted.")
    return redirect(url_for('index'))

@app.route('/sign_up', methods=GETPOST)
@logout_required
def sign_up() -> str:

    # display a form for user input
    signupform = SignupForm()

    # validate the form
    if signupform.validate_on_submit():
        # if the user has not properly confirmed their password
        if signupform.password.data != signupform.confirm_password.data:
            flash('Sign Up Error: Make sure "password" and "confirm password" are the same')
            return redirect(url_for('sign_up'))

        # else make a new user with the provided input from the form

        # put all the user data into this dict
        user_data = {"displayName" : signupform.display_name.data}

        try:
            create_firebase_user(
                  signupform.email.data
                , signupform.password.data
                , **user_data
            )

            pyre_auth.sign_in_with_email_and_password(signupform.email.data, signupform.password.data)

            # send an email verification
            pyre_auth.send_email_verification(pyre_auth.current_user)

            # flash back to the home page
            flash("Thank you for registering! Please go to your email and verify your account.")
            redirect(url_for('index'))


        except requests.exceptions.HTTPError as e:
            error_response = get_firebase_error_message(e)
            flash("Sign Up Error: %s" % error_map(error_response))
            return redirect(url_for("sign_up"))

    return render_template('signup.html', form=signupform, current_user_auth=current_user_auth, pyre_auth=pyre_auth, current_user_db=current_user_db)


@app.route('/log_in', methods=GETPOST)
@logout_required
def log_in() -> str:
    loginform = LoginForm()
    if loginform.validate_on_submit():
        # get the user
        try:
            sign_in_firebase_user(loginform.email.data, loginform.password.data)

            # flash back to the home page
            flash('welcome %s! you have logged in successfully' % current_user_db.get_property("displayName"))
            return redirect(url_for('index'))


        except requests.exceptions.HTTPError as e:
            error_response = get_firebase_error_message(e)
            flash("Log In Error: %s" % error_map(error_response))
            return redirect(url_for(log_in))

    return render_template('login.html', form=loginform, current_user_auth=current_user_auth, pyre_auth=pyre_auth, current_user_db=current_user_db)


@app.route('/resend_email_verification', methods=GETPOST)
@login_required
def resend_email_verification():
    current_user_auth.send_email_verification()
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
