import requests
from flask import url_for, flash, render_template
from flask_login import login_required, login_user, current_user
from markupsafe import Markup
from werkzeug.utils import redirect

from project import app
from project.forms.forms import SignupForm, verify_signup_form, LoginForm
from project.models.new_user_data import new_user_data
from project.auth.firebase_auth_errors import get_firebase_error_message, error_map
from project.auth.firebase_login import sign_out_firebase_user, delete_current_firebase_user, create_firebase_user, \
    sign_in_firebase_user
from project.views.home_views import GETPOST
from project.views.view_decorators import logout_required


@app.route('/log_out')
@login_required
def log_out() -> str:
    sign_out_firebase_user()
    return redirect(url_for('index'))


@app.route('/delete_account')
@login_required
def delete_account() -> str:
    delete_current_firebase_user()
    flash("your account has been deleted.")
    return redirect(url_for('index'))


def bulletize_messages(messages: list):
    bulleted_messages = ["<li>%s</li>" % m for m in messages]
    return "<ul>%s</ul>" % '\n'.join(bulleted_messages)


def title_and_messages(title: str, messages: list):
    return Markup("<h2>%s</h2><br/>%s" % (title, bulletize_messages(messages)))


@app.route('/sign_up', methods=GETPOST)
@logout_required
def sign_up() -> str:

    # display a form for user input
    signupform = SignupForm()

    # validate the form
    if signupform.validate_on_submit():
        # if the user has not properly confirmed their password
        signup_form_errors = verify_signup_form(signupform)
        if signup_form_errors:
            flash(title_and_messages("Sign Up Error", signup_form_errors))
            return redirect(url_for('sign_up'))

        # else make a new user with the provided input from the form

        # put all the user data into this dict
        user_data = new_user_data(display_name=signupform.display_name.data, e_mail=signupform.email.data)

        try:
            create_firebase_user(
                  signupform.email.data
                , signupform.password.data
                , **user_data
            )

            user = sign_in_firebase_user(signupform.email.data, signupform.password.data)
            login_user(user, remember=signupform.remember.data)

            # send an email verification
            current_user.send_email_verification()

            # flash back to the home page
            flash("Thank you for registering! Please go to your email and verify your account.")
            redirect(url_for('index'))


        except requests.exceptions.HTTPError as e:
            error_response = get_firebase_error_message(e)
            flash("Sign Up Error: %s" % error_map(error_response))
            return redirect(url_for("sign_up"))

    return render_template('signup.html', form=signupform)


@app.route('/log_in', methods=GETPOST)
@logout_required
def log_in() -> str:
    loginform = LoginForm()
    if loginform.validate_on_submit():
        # get the user
        try:
            user = sign_in_firebase_user(loginform.email.data, loginform.password.data)
            login_user(user, remember=loginform.remember.data)
            # flash back to the home page
            flash('welcome %s! you have logged in successfully' % current_user.get_db_property("displayName"))
            return redirect(url_for('index'))


        except requests.exceptions.HTTPError as e:
            error_response = get_firebase_error_message(e)
            flash("Log In Error: %s" % error_map(error_response))
            return redirect(url_for("log_in"))

    return render_template('login.html', form=loginform)


@app.route('/resend_email_verification', methods=GETPOST)
@login_required
def resend_email_verification():
    if current_user.get_auth_property("emailVerified"):
        flash("you have already verified your email!")
        return redirect(url_for("index"))

    current_user.send_email_verification()
    flash("email verification resent!")
    return redirect(url_for("index"))