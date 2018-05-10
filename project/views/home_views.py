'''
home_views.py

    routes for the home page and user settings

'''

from flask import render_template, flash
from flask_login import login_required, current_user

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
    if form.validate_on_submit() and form.display_name.data:
        current_user.set_db_property("displayName", form.display_name.data)
        flash("Display name successfully changed!")

    return render_template("edit_profile.html", form=form)