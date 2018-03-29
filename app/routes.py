from app import app, lm, fb_admin, pyre_auth, pyre_db
from .forms import LoginForm, SignupForm
from .user import user_from_admin, user_from_pyre, FirebaseUser, LoginUserError

from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, UserMixin, logout_user, login_required
from firebase_admin import auth as admin_auth

import requests

GETPOST = ['GET', 'POST']

### HOME PAGE ###
@app.route('/')
@app.route('/index')
def index() -> str:
    if current_user.is_authenticated:
        print(current_user)
        # render_template("index.html", user=current_user)
    return render_template("index.html")

### ERROR HANDLING ###
@app.errorhandler(404)
def not_found_error(error):
    return "page not found 404 error: " % (error), 404

@app.errorhandler(500)
def internal_error(error):
    return "internal server 500 error: " % (error), 500
    
### USER CREATION AND AUTHENTICATION ###
def check_and_login(user: FirebaseUser, form: LoginForm) -> str:
    # if the user creation is unsuccessful for some reason
    if user is None:
        raise LoginUserError
    
    # log in the user and go to index
    print("user data", user.email, user.id, user.display_name)
    print("user type", type(user))
    login_user(user, remember=form.remember.data)
    flash('welcome %s! you have logged in successfully' % user.id)
    return redirect(url_for('index'))

@app.route('/log_out')
def log_out() -> str:
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/log_in', methods=GETPOST)
def log_in() -> str:
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    loginform = LoginForm()
    if loginform.validate_on_submit():
        # process form data to log user in
        try:
            pyre_user = pyre_auth.sign_in_with_email_and_password(loginform.email.data, loginform.password.data)
            user = user_from_pyre(pyre_user) # convert the pyre_user json object to a FirebaseUser
            return check_and_login(user, loginform)
        except Exception as e:
            if type(e) == requests.exceptions.HTTPError:
                flash_content = e["message"]
            else:
                flash_content = e
                
            flash("Log In Error: %s" % flash_content)
            redirect(url_for('log_in'))            

    return render_template('login.html', form=loginform)

@app.route('/sign_up', methods=GETPOST)
def sign_up() -> str:
    signupform = SignupForm()
    if signupform.validate_on_submit(): 
        # if the user has not properly confirmed their password
        if signupform.password.data != signupform.confirm_password.data:
            flash('Sign Up Error: Make sure "password" and "confirm password" are the same')
            return redirect(url_for('sign_up'))
        
        # else make a new user with the provided input from the form
        try:
            admin_user = admin_auth.create_user(
                      app=fb_admin
                    , email=signupform.email.data
                    , email_verified=True # implement email verification later
                    , password=signupform.password.data
                    , uid=signupform.uid.data 
                   )
            print(admin_user)
            user = user_from_admin(admin_user) # convert the admin_user json object to a FirebaseUser
            return check_and_login(user, signupform)
        except Exception as e:
            flash("Error: %s" % e)
            redirect(url_for('sign_up'))
            
    return render_template('signup.html', form=signupform)

### GAME ROOMS ###
@app.route('/play_random')
def play_random() -> str:
    return 'play random'

@app.route('/play_friend')
def play_friend() -> str:
    return 'play friend'
