"""
edit_profile_form.py

    form for editing your profile

"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField


class EditProfileForm(FlaskForm):
    display_name = StringField()
    bio = TextAreaField()
    submit = SubmitField()
