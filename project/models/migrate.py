"""
migrate.py

tools for updating items in the database
"""
from project import pyre_db
import os

USER_BRANCH = os.getenv("USER_BRANCH") or "users"
ROOM_BRANCH = os.getenv("ROOM_BRANCH") or "SuicideChess"

def add_branch_property(branch_name: str, property_name: str, default_value):
    '''
    add a new property for each user
    :param property_name:
    :param default_value:
    :return:
    '''

    children = pyre_db.child(branch_name).get().val()
    if children:
        for child_id, child_data in children.items():
            child_data[property_name] = default_value
            pyre_db.child(branch_name).child(child_id).set(child_data)


def add_user_property(property_name: str, default_value):
    add_branch_property(USER_BRANCH, property_name, default_value)

def add_room_property(property_name: str, default_value):
    add_branch_property(ROOM_BRANCH, property_name, default_value)