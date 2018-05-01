'''
forms.py

all the forms throughout the project. maybe if we have too many forms, we can split this into multiple files.
'''

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Email

from project.forms.worst_passwords import WORST_PASSWORDS, TOTAL_WORST_PASSWORDS

class LoginForm(FlaskForm):
    email = StringField("email", [InputRequired("Please enter your email address."), Email("Please enter a valid email address.")])
    password = PasswordField("password", [InputRequired("Please enter your password.")])
    remember = BooleanField("remember me")
    submit = SubmitField()

class SignupForm(LoginForm):
    display_name = StringField("display name")
    confirm_password = PasswordField("confirm password", [InputRequired("Please confirm your password.")])

def verify_signup_form(signupform: SignupForm):
    password, confirm_password = signupform.password.data, signupform.confirm_password.data
    conditions = {
          "Make sure the password and confirm password fields are the same." : password == confirm_password
        , "Your password must be at least 8 characters." : len(password) > 7
        , "Do not use one of the worst %s passwords." % TOTAL_WORST_PASSWORDS : password not in WORST_PASSWORDS
    }
    # return a list of false conditions
    return [message for message in conditions if not conditions[message]]
