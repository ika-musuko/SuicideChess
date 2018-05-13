"""
firebase_user.py

handling the firebase authentication module.
deals with sending and receiving data from the firebase authentication module and also login persistence

"""

from flask_login import UserMixin
from project import pyre_db, lm
from project.models.new_user_data import new_user_data

# append this string at the beginning of invalid character replacement
CONVERTER_STRING = "zHGHGHGHGzz"

class InvalidEmailAddress(Exception):
    '''
    throw this exception if the user's email is invalid
    '''
    pass

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

# functions to get user objects
def to_user_key(email: str) -> str:
    '''
    converts an email into a usable database key

    Illegal characters to convert
    . (period)
    $ (dollar sign)
    [ (left square bracket)
    ] (right square bracket)
    # (hash or pound sign)
    / (forward slash)

    :param email:
    :return:

    '''
    user_key = email.split("@")[0]
    replace_dict = {
         ".": CONVERTER_STRING+"PERIODzzz"
        ,"$": CONVERTER_STRING+"DOLLARzzz"
        ,"[": CONVERTER_STRING+"LBRACKETzzz"
        ,"]": CONVERTER_STRING+"RBRACKETzzz"
        ,"#": CONVERTER_STRING+"HASHPOUNDzzz"
        ,"/": CONVERTER_STRING+"FORWARDSLASHzzz"
    }

    # replace all of the invalid characters
    for char, repl in replace_dict.items():
        user_key = user_key.replace(char, repl)

    return user_key


def get_firebase_user_by_email(email: str):
    """
    check if a Firebase user already exists by email and return it
    if they don't return None
    :param email:
    :return:
    """
    # get the user id from the userKeys
    user_key = to_user_key(email)
    user_id = pyre_db.child("userKeys").child(user_key).get().val()
    return get_firebase_user(user_id)


def get_firebase_user(user_id: str):
    # if the user id exists
    if user_id:
        # check if the user exists in the database
        if pyre_db.child("users").child(user_id).get().val():
            return FirebaseUser(user_id)

    # return None if they don't exist
    return None


def create_firebase_user(display_name: str, email: str):
    """
    create a new firebase user with a display_name and user_id

    :param display_name:
    :param email:
    :return:
    """
    # prevent people from exploiting the converter string to log in as another user
    if CONVERTER_STRING in email:
        raise InvalidEmailAddress

    # get the user key
    user_key = to_user_key(email)

    # get a new user ID for the user
    total_users = pyre_db.child("userKeys").child("TOTAL_USERS").get().val()

    # increment the total amount of users
    total_users = total_users + 1 if total_users else 1
    pyre_db.child("userKeys").child("TOTAL_USERS").set(total_users)

    # make a new user id
    user_id = ''.join(("u", str(total_users)))

    # add the user's email to the user keys
    pyre_db.child("userKeys").child(user_key).set(user_id)

    # add the user to the database
    new_user = new_user_data(display_name=display_name, e_mail=email)
    pyre_db.child("users").child(user_id).set(new_user) # use user_id as key (list)

    return FirebaseUser(user_id)

