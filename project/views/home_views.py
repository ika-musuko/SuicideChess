'''
home_views.py

    routes for the home page and user settings

'''

from flask import render_template
from flask_login import login_required

from project import app

from project.forms.edit_profile_form import EditProfileForm
from project.views.view_utils import GETPOST

### HOME PAGE ###
@app.route('/')
@app.route('/index')
def index() -> str:
    return render_template("index.html")

### EDIT PROFILE ###
@app.route('/edit_profile', methods=GETPOST)
@login_required
def edit_profile() -> str:
    form = EditProfileForm()
    return render_template("edit_profile.html", form=form)