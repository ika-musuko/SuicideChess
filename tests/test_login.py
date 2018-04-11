import unittest
import pdb

from flask_login import login_user, current_user

from project import app, pyre_auth
from project.auth.firebase_login import sign_in_firebase_user \
    , create_firebase_user \
    , delete_current_firebase_user \
    , current_user_auth \
    , current_user_db \
    , user_loader_helper


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = True
        self.response_token = None

    def _create_user(self, email, password, displayName):
        print("creating a user...")
        self.response_token = create_firebase_user(email, password, displayName=displayName)
        print("user created successfully!")

    def _create_and_sign_in_user(self, email, password, displayName):
        self._create_user(email, password, displayName)
        self.response_token = None
        print("logging in user...")
        sign_in_firebase_user(email, password)


    def test_account_creation(self):
        self._create_and_sign_in_user("ytgoluigi2196@gmail.com", "drakeiscool", "drake")
        print("logging in user...")
        sign_in_firebase_user("ytgoluigi2196@gmail.com", "drakeiscool")
        assert(pyre_auth.current_user is not None)
        print("user logged in successfully!")

        print("user info")
        print("\t(from auth) email address: ", current_user_auth.get_property("email"))
        print("\t(from auth) email verified: ", current_user_auth.get_property("emailVerified"))
        print("\t(from db) display name: ", current_user_db.get_property("displayName"))

    def test_email_verification(self):
        self._create_and_sign_in_user("ytgoluigi2196@gmail.com", "drakeiscool", "drake")

        print("send verification email")
        current_user_auth.send_email_verification()
        print("email sent!")
        print("email verified: ", current_user_auth.get_property("emailVerified"))
        input("Please go to the email address and verify the email and then press any key to continue")
        print("email verified: ", current_user_auth.get_property("emailVerified"))

    def test_flask_login_integration(self):
    
        self._create_and_sign_in_user("ytgoluigi2196@gmail.com", "drakeiscool", "drake")

        print("signing in the user into firebase auth...")
        with app.test_request_context():
            user = sign_in_firebase_user("ytgoluigi2196@gmail.com", "drakeiscool")
            print("logging the user into flask...")
            login_user(user)
            print("current user authenticated?")
            assert(current_user.is_authenticated)
            print("invalidating the user token... (this is like if the authentication token expires, for example)")
            pyre_auth.current_user['idToken'] = "fail"
            print("reloading the user...")
            user_loader_helper()
            assert(pyre_auth.current_user['idToken'] != "fail")
            assert(current_user.is_authenticated)
            print("flask login passed!")

    def tearDown(self):
        print("tearing down...")
        delete_current_firebase_user(self.response_token)

if __name__ == '__main__':
    unittest.main()