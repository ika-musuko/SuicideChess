from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField, PasswordField
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    email = StringField("email", [InputRequired("Please enter your email address."), Email("Please enter a valid email address.")])
    password = PasswordField("password", [InputRequired("Please enter your password.")])
    remember = BooleanField("remember me")
    submit = SubmitField()

class SignupForm(LoginForm):
    display_name = StringField("display name")
    confirm_password = PasswordField("confirm password", [InputRequired("Please confirm your password.")])