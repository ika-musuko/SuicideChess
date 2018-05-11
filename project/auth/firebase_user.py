"""
firebase_user.py

handling the firebase authentication module.
deals with sending and receiving data from the firebase authentication module and also login persistence

"""

from flask_login import UserMixin
from project import pyre_db, lm
from project.models.new_user_data import new_user_data


def get_firebase_user(user_id: str):
    """
    check if a Firebase user already exists and return it
    if they don't return None
    :param user_id:
    :return:
    """
    # check if the user exists in the database
    if pyre_db.child("users").child(user_id).get().val():
        return FirebaseUser(user_id)

    # return None if they don't exist
    return None


def create_firebase_user(display_name: str, user_id: str):
    """
    create a new firebase user with a display_name and user_id

    :param display_name:
    :param user_id:
    :return:
    """
    new_user = new_user_data(display_name=display_name, e_mail=user_id)
    pyre_db.child("users").child(user_id).set(new_user)

    return FirebaseUser(user_id)


# session management via Flask-Login
@lm.user_loader
def user_loader(user_id):
    return get_firebase_user(user_id)


class FirebaseUser(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    # UserMixin overload
    def get_id(self):
        return self.id

    def get_db_property(self, property: str):  # gets database property -joleena
        return pyre_db.child("users").child(self.id).child(property).get().val()

    def set_db_property(self, property: str, value):
        pyre_db.child("users").child(self.id).child(property).set(value)

    def as_dict(self):
        """
        get the user data as a dict
        :return:
        """
        return pyre_db.child("users").child(self.id).get().val()

    @property
    def display_name(self):
        return self.get_db_property("displayName")
