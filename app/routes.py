from app import app, lm
from .forms import LoginForm, SignupForm

from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/log_in')
def log_in():
    loginform = LoginForm()
    return render_template("login.html", form=loginform)

@app.route('/sign_up')
def sign_up():
    signupform = SignupForm()
    return render_template("signup.html", form=signupform)

@app.route('/play_random')
def play_random():
    return 'play random'

@app.route('/play_friend')
def play_friend():
    return 'play friend'
