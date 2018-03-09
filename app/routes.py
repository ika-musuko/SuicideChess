from app import app, lm, fb_admin, pyre_auth, pyre_db
from .forms import LoginForm, SignupForm

from flask import render_template, flash
from flask_login import current_user, login_user
from firebase_admin import auth as admin_auth

GETPOST = ['GET', 'POST']

### HOME PAGE ###
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

### USER CREATION AND AUTHENTICATION ###
def check_and_login(user, form: LoginForm):
    # if the user creation is unsuccessful for some reason
    if user is None:
        flash('could not create user')
    
    # log in the user and go to index
    login_user(user, remember=form.remember.data)
    return redirect(url_for('index'))

@app.route('/log_in', methods=GETPOST)
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    loginform = LoginForm()
    if loginform.validate_on_submit():
        # process form data to log user in
        user = pyre_auth.sign_in_with_email_and_password(loginform.email.data, loginform.password.data)
        return check_and_login(user, loginform)

    return render_template('login.html', form=loginform)

@app.route('/sign_up', methods=GETPOST)
def sign_up():
    signupform = SignupForm()
    if signupform.validate_on_submit(): 
        # if the user has not properly confirmed their password
        if signupform.password.data != signupform.confirm_password.data:
            flash('Make sure "password" and "confirm password" is the same')
            return redirect(url_for('sign_up'))
        
        # else make a new user with the provided input from the form
        user = admin_auth.create_user(
                  app=fb_admin
                , email=signupform.email.data
                , email_verified=True # implement email verification later
                , password=signupform.password.data
                , uid=signupform.uid.data 
               )
        return check_and_login(user, signupform)

    return render_template('signup.html', form=signupform)

### GAME ROOMS ###
@app.route('/play_random')
def play_random():
    return 'play random'

@app.route('/play_friend')
def play_friend():
    return 'play friend'
