from app import app, lm, pyre_auth, pyre_db
from .forms import LoginForm, SignupForm
from .firebase_login import sign_in_firebase_user, create_firebase_user
from .utils import get_firebase_error_message
from .error_maps import error_map

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

import requests

GETPOST = ['GET', 'POST']


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
    logout_user()
    return redirect(url_for('index'))


@app.route('/sign_up', methods=GETPOST)
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
        # create the user
        user_data = {"displayName" : signupform.display_name.data}

        try:
            user = create_firebase_user(
                  signupform.email.data
                , signupform.password.data
                , **user_data
            )

            # log in the user
            login_user(user, remember=signupform.remember.data)

            # send an email verification
            user.send_email_verification()

            # flash back to the home page
            flash("Thank you for registering! Please go to your email and verify your account.")
            redirect(url_for('index'))


        except requests.exceptions.HTTPError as e:
            error_response = get_firebase_error_message(e)
            flash("Sign Up Error: %s" % error_map(error_response))
            return render_template('signup.html', form=signupform)

    return render_template('signup.html', form=signupform)


@app.route('/log_in', methods=GETPOST)
def log_in() -> str:
    if current_user.is_authenticated:
        flash("you are already logged in")
        return redirect(url_for('index'))

    loginform = LoginForm()
    if loginform.validate_on_submit():
        # get the user
        try:
            user = sign_in_firebase_user(loginform.email.data, loginform.password.data)
            print(user)
            login_user(user)

            # flash back to the home page
            flash('welcome %s! you have logged in successfully' % current_user.displayName)
            return redirect(url_for('index'))


        except requests.exceptions.HTTPError as e:
            error_response = get_firebase_error_message(e)
            flash("Log In Error: %s" % error_map(error_response))
            return render_template('login.html', form=loginform)

    return render_template('login.html', form=loginform)


@app.route('/resend_email_verification', methods=GETPOST)
@login_required
def resend_email_verification():
    current_user.send_email_verification()
    flash("email verification resent!")
    return url_for("index")

### GAME ROOMS ###
@app.route('/play_random')
@login_required
def play_random() -> str:
    return 'play random'


@app.route('/play_friend')
@login_required
def play_friend() -> str:
    return 'play friend'
