from flask_login import UserMixin
from firebase_admin import auth
from app import lm, fb_admin

class LoginUserError(Exception):
    def __str__(self):
        return "could not login the user (LoginUserError)"

class FirebaseUser(UserMixin):
    def __init__(self, email: str, uid: str, display_name: str):
        '''
            email: str
            uid: str
            display_name: str
        '''
        self.email = email
        self.id = uid
        self.display_name = display_name
        #self.user_metadata = user_metadata

    # @property
    # def is_authenticated(self):
        # return True

    # @property
    # def is_active(self):
        # return True

    # @property
    # def is_anonymous(self):
        # return False

    # @property
    # def get_id(self):
        # return self.uid


@lm.user_loader
def user_loader(uid: str) -> FirebaseUser:
    # load user from firebase
    return user_from_admin(auth.get_user(uid, app=fb_admin))
    
# functions to convert firebase auth objects into flask_login compliant FirebaseUser objects    
def user_from_admin(admin_user: auth.UserRecord) -> FirebaseUser:
    return FirebaseUser(
                              email=admin_user.email
                            , uid=admin_user.uid
                            , display_name=admin_user.display_name
                            #, user_metadata=admin_user.user_metadata
                       )

def user_from_pyre(pyre_user: dict) -> FirebaseUser:
    return FirebaseUser(
                              email=pyre_user['email']
                            , uid=pyre_user['localId']
                            , display_name=pyre_user['displayName']
                            #, user_metadata=admin_user.user_metadata
                       )