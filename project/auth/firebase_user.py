'''
firebase_user.py

handling the firebase authentication module.
deals with sending and receiving data from the firebase authentication module and also login persistence

SORRY HALF OF THIS CODE IS JUST HACKS LOL
'''

from flask_login import UserMixin
from project import pyre_db, lm
from project.models.new_user_data import new_user_data


def get_firebase_user(email: str):
    '''
    check if a Firebase user already exists and return it
    if they don't return None
    :param email:
    :return:
    '''
    # check if the user exists in the database
    if pyre_db.child("users").child(email).get().val():
        return FirebaseUser(email)

    # return None if they don't exist
    return None


def create_firebase_user(display_name: str, email: str):
    '''
    create a new firebase user with a display_name and email

    :param display_name:
    :param email:
    :return:
    '''
    new_user = new_user_data(display_name=display_name, e_mail=email)
    pyre_db.child("users").child(email).set(new_user)

    return FirebaseUser(email)


# session management via Flask-Login
@lm.user_loader
def user_loader(email):
    return get_firebase_user(email)

class FirebaseUser(UserMixin):
    def __init__(self, email):
        self.id = email

    def get_db_property(self, property: str):    #gets database property -joleena
        return pyre_db.child("users").child(self.id).child(property).get().val()

    def set_db_property(self, property: str, value):
        pyre_db.child("users").child(self.id).child(property).set(value)

    def get_id(self):
        return self.id



