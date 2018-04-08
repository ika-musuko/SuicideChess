from app import app, lm, pyre_auth, pyre_db
from .forms import LoginForm, SignupForm
from .firebase_login import sign_in_firebase_user, create_firebase_user

from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user


import json

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
        user_data = {"display_name" : signupform.display_name.data}

        user = create_firebase_user(
              signupform.email.data
            , signupform.password.data
            , user_data=user_data
        )

        print(user)
        print(user.auth_data)

        # log in the user
        login_user(user, remember=signupform.remember.data)

        # send an email verification
        user.send_email_verification()

        # flash back to the home page
        flash("Thank you for registering! Please go to your email and verify your account.")
        redirect(url_for('index'))

    return render_template('signup.html', form=signupform)


@app.route('/log_in', methods=GETPOST)
def log_in() -> str:
    loginform = LoginForm()
    if loginform.validate_on_submit():
        # process form data to log user in
        # get the user
        user = sign_in_firebase_user(loginform.email.data, loginform.password.data)
        print(user)
        print(user.keys())

        # flash back to the home page
        flash('welcome %s! you have logged in successfully' % user.display_name)
        return redirect(url_for('index'))

    return render_template('login.html', form=loginform)


@app.route('/resend_email_verification', methods=GETPOST)
def resend_email_verification():
    current_user.send_email_verification()
    flash("email verification resent!")
    return url_for("index")

### GAME ROOMS ###
@app.route('/play_random')
def play_random() -> str:
    return 'play random'


@app.route('/play_friend')
def play_friend() -> str:
    return 'play friend'
