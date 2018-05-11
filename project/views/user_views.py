'''
user_views.py

    routes for the home page and user settings

'''

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from project import app, player_manager
from project.players import player_exceptions
from project.forms.edit_profile_form import EditProfileForm
from project.views.view_utils import GETPOST

### HOME PAGE ###
@app.route('/')
@app.route('/index')
def index() -> str:
    '''
    show the user's own profile
    :return:
    '''
    return render_template("index.html")

### ALL USERS ###
@app.route('/all_users')
def all_users() -> str:
    all_user_ids = player_manager.get_all_user_ids()
    return render_template("all_users.html", all_user_ids=all_user_ids)


### VIEW PROFILE ###
@app.route('/user/<user_id>')
def user(user_id: str) -> str:
    '''
    view for showing another user's profile page
    :param user_id:
    :return:
    '''
    try:
        user = player_manager.get_user(user_id)
        return render_template("user.html", user=user, user_id=user_id)

    except player_exceptions.PlayerNotFound:
        flash("This user does not exist.")
        return redirect(url_for("index"))


### EDIT PROFILE ###
@app.route('/edit_profile', methods=GETPOST)
@login_required
def edit_profile() -> str:
    '''
    edit a profile
    :return:
    '''
    form = EditProfileForm()
    if form.validate_on_submit():
        # only update their display name if it's not blank
        if form.display_name.data:
            current_user.set_db_property("displayName", form.display_name.data)

        # only update their bio if it's not blank
        if form.bio.data:
            current_user.set_db_property("bio", form.bio.data)

        flash("Profile successfully changed!")

    return render_template("edit_profile.html", form=form)