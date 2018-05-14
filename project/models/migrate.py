"""
migrate.py

tools for updating items in the database
"""
from project import pyre_db

def add_user_property(property_name: str, default_value):
    '''
    add a new property for each user
    :param property_name:
    :param default_value:
    :return:
    '''

    users = pyre_db.child("users").get().val()
    if users:
        for user_id, user_data in users.items():
            user_data[property_name] = default_value
            pyre_db.child("users").child(user_id).set(user_data)

