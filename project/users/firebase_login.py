'''
firebase_login.py
'''

import requests
from firebase_admin import auth as fb_auth
from flask_login import UserMixin, logout_user, current_user

from project import pyre_db, pyre_auth, lm, fb_admin


### pyrebase wrappers
# sign_in_with_email_and_password(email, password)
def sign_in_firebase_user(email: str, password: str):
    # get the users data
    pyre_auth.sign_in_with_email_and_password(email, password)
    refresh_current_user()
    return FirebaseUser()

# create_user_with_email_and_password(email, password)
def create_firebase_user(e_mail: str, password: str, **user_data):
    # create a new authentication account
    response_token = pyre_auth.create_user_with_email_and_password(e_mail, password)

    # add the new user data to the database
    pyre_db.child("users").child(response_token["localId"]).set(user_data, response_token['idToken'])
    return response_token

# sign out user (also handles logout_user) DON'T USE logout_user by itself!!
def sign_out_firebase_user():
    logout_user()
    pyre_auth.current_user = None

# delete_user_account
def delete_current_firebase_user(response_token=None):
    auth_token = pyre_auth.current_user or response_token
    try:
        if auth_token:
            pyre_db.child("users").child(auth_token["localId"]).remove(auth_token['idToken'])
            pyre_auth.delete_user_account(auth_token['idToken'])
    except requests.exceptions.HTTPError:
        refresh_current_user()
        pyre_db.child("users").child(pyre_auth.current_user["localId"]).remove(pyre_auth.current_user['idToken'])
        pyre_auth.delete_user_account(pyre_auth.current_user['idToken'])

# refresh current user
def refresh_current_user():
    pyre_auth.refresh_current_user(pyre_auth.current_user["refreshToken"])

### user users actions
class current_user_auth:
    @staticmethod
    def get_property(property: str):
        return pyre_auth.get_user_property(pyre_auth.current_user['idToken'], property)

    @staticmethod
    def send_email_verification():
        return pyre_auth.send_email_verification(pyre_auth.current_user['idToken'])

### user data from database
class current_user_db:
    @staticmethod
    def get_property(property: str):
        return pyre_db.child("users").child(pyre_auth.current_user['localId']).child(property).get().val()


### flask_login support
@lm.user_loader
def user_loader(dummy):
    return user_loader_helper()

def user_loader_helper():
    if not pyre_auth.current_user:
        return None

    if not current_user_db.get_property("displayName"):
        return None

    try:
        parsed_jwt = fb_auth.verify_id_token(pyre_auth.current_user['idToken'], app=fb_admin)
        return FirebaseUser()
    except ValueError:
        refresh_current_user()
        return FirebaseUser()

class FirebaseUser(UserMixin):
    def get_auth_property(self, property: str):
        return current_user_auth.get_property(property)

    def get_db_property(self, property: str):
        return current_user_db.get_property(property)

    def send_email_verification(self):
        return current_user_auth.send_email_verification()

    # life hack LIFE HACK....L I F E H A C K
    # don't use this function for getting a user's id, use the get_user_id one
    def get_id(self):
        return True

