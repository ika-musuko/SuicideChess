import os
import unittest

from app import app, pyre_auth, pyre_db
from app.firebase_login import sign_in_firebase_user, create_firebase_user

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = True

    def test_user_login(self):
        print("creating a new user...")
        cuser = create_firebase_user("mariokart2196@gmail.com", "drakeiscool", displayName="drake")
        print(cuser.auth_data)
        print("creation successful!")

        print("signing in the new user...")
        cuser = sign_in_firebase_user("mariokart2196@gmail.com", "drakeiscool")
        print(cuser.auth_data)
        print("sign in successful!")

        print("sending an email verification to the user...")
        cuser.send_email_verification()
        print("check the email!")

        print("getting the data from the user")
        print(cuser.get_user_data())
        print("finished getting user data..,!")

        print("get a property...")
        print(cuser.get_property("displayName"))
        print("got a property!")

        print("all done with the user! deleting user...")
        cuser.delete()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()