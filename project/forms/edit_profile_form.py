'''
edit_profile_form.py

    form for editing your profile

'''

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField

from flask_login import current_user

class EditProfileForm(FlaskForm):
    display_name = StringField()

    def __init__(self, *args, **kwargs):
        if current_user.is_authenticated
            # init the form object
            super(EditProfileForm, self).__init__(*args, **kwargs)

            # form default data
            self.display_name.data = current_user.get_db_property("displayName")