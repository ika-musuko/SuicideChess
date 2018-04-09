import unittest
import pdb
import requests
import json

from flask_login import login_user, current_user, logout_user

from app import app, pyre_auth, pyre_db, lm
from app.utils import get_firebase_error_message
from app.firebase_login import FirebaseUser, sign_in_firebase_user, create_firebase_user
from app.utils import get_firebase_error_message

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = True

        self.cuser = None

    def test_user_database(self):
        print("creating a new user...")
        self.cuser = create_firebase_user("ytgoluigi2196@gmail.com", "drakeiscool", displayName="drake")
        print(self.cuser.auth_data)
        print("creation successful!")

        print("signing in the new user...")
        self.cuser = sign_in_firebase_user("ytgoluigi2196@gmail.com", "drakeiscool")
        print(self.cuser.auth_data)
        print("sign in successful!")

        print("sending an email verification to the user...")
        self.cuser.send_email_verification()
        print("check the email!")

        print("getting the data from the user")
        print(self.cuser.get_user_data())
        print("finished getting user data..,!")

        print("get a property...")
        print(self.cuser.get_property("displayName"))
        print("got a property!")

        print("all done with the user! deleting user...")

    def test_flask_login_integration(self):
        print("creating a new user...")
        self.cuser = create_firebase_user("ytgoluigi2196@gmail.com", "drakeiscool", displayName="drake")
        print("logging in the new user")
        with app.test_request_context():
            login_user(self.cuser, remember=True)
            print("current user data: ")
            print(current_user.get_user_data())
            print("getting a property which requires auth data... (true or false doesn't matter)")
            print(current_user.email_verified)
            print("logging out user")
            logout_user()

            print("now testing sign in")
            self.cuser = sign_in_firebase_user("ytgoluigi2196@gmail.com", "drakeiscool")
            login_user(self.cuser, remember=True)
            print("current user data: ")
            print(current_user.get_user_data())
            print("getting a property which requires auth data... (true or false doesn't matter)")
            print(current_user.email_verified)
            print("logging out user")
            logout_user()

        print("all done! tearing down")

    def test_wrong_password(self):
        self.cuser = create_firebase_user("ytgoluigi2196@gmail.com", "drakeiscool", displayName="drake")
        print(self.cuser.auth_data)
        try:
            self.cuser = sign_in_firebase_user("ytgoluigi2196@gmail.com", "wrongpassword")
        except requests.exceptions.HTTPError as e:
            print("HERE IS THE ERROR")
            print(type(e))
            print(get_firebase_error_message(e))

    def test_invalid_email(self):
        try:
            self.cuser = create_firebase_user("aaaaaaa", "aaa", displayName="asdfaaaaaa")
        except requests.exceptions.HTTPError as e:
            print(get_firebase_error_message(e))

    def test_get_email_verified(self):
        self.cuser = create_firebase_user("ytgoluigi2196@gmail.com", "drakeiscool", displayName="drake")
        print(self.cuser.email_verified)

    def tearDown(self):
        try:
            self.cuser.delete()
        except:
            pass

if __name__ == '__main__':
    unittest.main()