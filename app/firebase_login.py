'''
firebase_login.py
library for connecting flask-login with firebase's authentication and db system
'''

from flask_login import UserMixin
from app import lm, pyre_db, pyre_auth

import pdb

class LoginUserError(Exception):
    def __str__(self):
        return "could not login the user (LoginUserError)"

@lm.user_loader
def user_loader(id):
    user = pyre_db.child("users").child(id).get().val()
    if user is None:
        return None
    return FirebaseUser(id=id)


class FirebaseUser(UserMixin):
    def __init__(self, id, auth_data=None):
        self.id = id
        self.auth_data = auth_data

    def get_user(self):
        return pyre_db.child("users").child(self.id).get().val()

    def get_user_data(self):
        return pyre_db.child("users").child(self.id).get().val()

    def get_property(self, property: str):
        return pyre_db.child("users").child(self.id).child(property).get().val()

    def send_email_verification(self):
        pyre_auth.send_email_verification(self.auth_data['idToken'])

    def get_auth_info(self):
        return pyre_auth.get_account_info(self.auth_data['idToken'])

    def get_id(self):
        return self.id

    @property
    def displayName(self):
        return self.get_property("displayName")

    # requires pyrebase_ext
    def delete(self):
        pyre_db.child("users").child(self.id).remove(self.auth_data['idToken'])
        pyre_auth.delete_user_account(self.auth_data['idToken'])


# pyrebase wrappers

# sign_in_with_email_and_password(email, password)
def sign_in_firebase_user(email: str, password: str):
    # get the auth data
    auth_data = pyre_auth.sign_in_with_email_and_password(email, password)
    user_with_email = pyre_db.child("users").order_by_child("email").equal_to(email).limit_to_first(1).get()
    user_id = next(iter(user_with_email.val())) # get the top key

    # return the associated user
    return FirebaseUser(user_id, auth_data)


# create_user_with_email_and_password(email, password)
def create_firebase_user(email: str, password: str, **user_data):
    # get the auth data
    auth_data = pyre_auth.create_user_with_email_and_password(email, password)

    # get total users and use as id
    current_total_users = pyre_db.child("TOTAL_USERS").get().val()
    current_total_users += 1
    print(current_total_users, type(current_total_users))
    pyre_db.child("TOTAL_USERS").set(current_total_users)

    # add the new user data to the database
    user_data["email"] = email
    pyre_db.child("users").child(current_total_users).set(user_data, auth_data['idToken'])
    return FirebaseUser(current_total_users, auth_data)