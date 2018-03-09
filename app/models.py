from flask_login import UserMixin
from app import lm 

class User(UserMixin):
    pass

@lm.user_loder
def user_loader(email):
    
