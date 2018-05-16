"""
migrate.py

tools for updating items in the database
"""
from project import pyre_db
import os

USER_BRANCH = os.getenv("USER_BRANCH") or "users"
ROOM_BRANCH = os.getenv("ROOM_BRANCH") or "SuicideChess"


def add_branch_property(branch_name: str, property_name: str, default_value):
    """
    add a new property for each user
    :param branch_name:
    :param property_name:
    :param default_value:
    :return:
    """

    children = pyre_db.child(branch_name).get().val()
    if children:
        for child_id, child_data in children.items():
            if not pyre_db.child(branch_name).child(child_id).get().val():
                child_data[property_name] = default_value
                pyre_db.child(branch_name).child(child_id).set(child_data)


def add_user_property(property_name: str, default_value):
    add_branch_property(USER_BRANCH, property_name, default_value)


def add_room_property(property_name: str, default_value):
    add_branch_property(ROOM_BRANCH, property_name, default_value)


def do_migrate():
    import project  # init project
    # write any migrate code here
    # set the environment variables
    # run using run_migration.sh in the root folder

    # users = pyre_db.child("users").get().val()
    # for user_id, user_data in users.items():
    #     print(user_id)
    #     if "gameHistories" in user_data:
    #         print(" game histories exist")
    #         game_histories = user_data["gameHistories"]
    #         if game_histories:
    #             for room_id, game_history in game_histories.items():
    #                 print("  ",room_id)
    #                 if "lastBoard" not in game_history:
    #                     print("    adding last board")
    #                     last_board = {
    #                         "black_bishopA":{"x":2,"y":0},
    #                         "black_bishopB":{"x":5,"y":0},"black_king":{"x":4,"y":0},"black_knightA":{"x":1,"y":0},
    #                         "black_knightB":{"x":6,"y":0},"black_pawnA":{"firstMove":True,"x":0,"y":1},"black_pawnB":{"firstMove":True,"x":1,"y":1},
    #                         "black_pawnC":{"firstMove":True,"x":2,"y":1},"black_pawnD":{"firstMove":True,"x":3,"y":1},"black_pawnE":{"firstMove":True,"x":4,"y":1},
    #                         "black_pawnF":{"firstMove":True,"x":5,"y":1},"black_pawnG":{"firstMove":True,"x":6,"y":1},"black_pawnH":{"firstMove":True,"x":7,"y":1},
    #                         "black_queen":{"x":3,"y":0},"black_rookA":{"x":0,"y":0},"black_rookB":{"x":7,"y":0},
    #                         "whiteTurn":True,"white_bishopA":{"x":2,"y":7},"white_bishopB":{"x":5,"y":7},"white_king":{"x":4,"y":7},
    #                         "white_knightA":{"x":1,"y":7},"white_knightB":{"x":6,"y":7},"white_pawnA":{"firstMove":True,"x":0,"y":6},
    #                         "white_pawnB":{"firstMove":True,"x":1,"y":6},"white_pawnC":{"firstMove":True,"x":2,"y":6},"white_pawnD":{"firstMove":True,"x":3,"y":6},
    #                         "white_pawnE":{"firstMove":True,"x":4,"y":6},"white_pawnF":{"firstMove":True,"x":5,"y":6},"white_pawnG":{"firstMove":True,"x":6,"y":6},
    #                         "white_pawnH":{"firstMove":True,"x":7,"y":6},"white_queen":{"x":3,"y":7},"white_rookA":{"x":0,"y":7},
    #                         "white_rookB":{"x":7,"y":7}
    #                     }
    #                     pyre_db.child("users").child(user_id).child("gameHistories").child(room_id).child("lastBoard").set(last_board)

    ### epilog code here
    print("leaving do_migrate()")
