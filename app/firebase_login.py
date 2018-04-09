'''
firebase_login.py
'''

from app import pyre_db, pyre_auth
import pdb

### pyrebase wrappers
# sign_in_with_email_and_password(email, password)
def sign_in_firebase_user(email: str, password: str):
    # get the auth data
    pyre_auth.sign_in_with_email_and_password(email, password)

# create_user_with_email_and_password(email, password)
def create_firebase_user(email: str, password: str, **user_data):
    # create a new authentication account
    response_token = pyre_auth.create_user_with_email_and_password(email, password)

    # add the new user data to the database
    user_data["email"] = email
    pyre_db.child("users").child(response_token["localId"]).set(user_data, response_token['idToken'])
    return response_token

# delete_user_account
def delete_current_firebase_user(response_token=None):
    auth_token = pyre_auth.current_user or response_token
    if auth_token:
        pyre_db.child("users").child(auth_token["localId"]).remove(auth_token['idToken'])
        pyre_auth.delete_user_account(auth_token['idToken'])

### user auth actions
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
