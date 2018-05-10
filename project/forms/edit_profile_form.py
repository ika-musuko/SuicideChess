'''
edit_profile_form.py

    form for editing your profile

'''

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField

from flask_login import current_user

class EditProfileForm(FlaskForm):
    display_name = StringField()
    submit = SubmitField()

