### NEW GAME DATA ###
# make this dict the default data of a new game once the game data spec has been completed
# just replace it
from collections import OrderedDict
import pdb
from functools import wraps

class RoomDoesNotExist(Exception):
    pass

class RoomIsInProgress(Exception):
    pass

class RoomIsNotFriend(Exception):
    pass

class RoomManager:
    def __init__(self, db, game_branch, new_game_data):
        self.pyre_db = db
        self.game_branch = game_branch
        self.new_game_data = new_game_data

    # all these methods should return an (str, dict) tuple containing (game_id, room_data)
    def new_room(self, players: list, mode: str, variant: str, status: str="waiting") -> (str, dict):
        # get the latest game number and use as an ID
        total_games = self.pyre_db.child(self.game_branch).child("TOTAL_GAMES").get().val()
        if not total_games:
            self.pyre_db.child(self.game_branch).child("TOTAL_GAMES").set(0)
            total_games = 0
        total_games += 1
        self.pyre_db.child(self.game_branch).child("TOTAL_GAMES").set(total_games)
        assigned_room_id = "Room%s" % total_games

        # add a new game room
        room_data = {
              "players" : players
            , "variant" : variant
            , "status" : status
            , "mode"   : mode
            , "gameData" : self.new_game_data
        }
        self.pyre_db.child(self.game_branch).child(assigned_room_id).set(room_data)
        return assigned_room_id, room_data


    # RANDOM mode
    def join_random_game(self, display_name: str, variant: str) -> (str, dict):
        db_query = self.pyre_db.child(self.game_branch)\
            .order_by_child("mode").equal_to("random")\
            .order_by_child("status").equal_to("waiting")\
            .limit_to_first(2).get()
        branch, open_rooms = db_query.key(), db_query.val()

        if not open_rooms:
            return self.new_room([display_name], "random", variant)

        # get the top room from the open rooms
        open_room_key = next(iter(open_rooms))
        open_room = open_rooms[open_room_key]

        # change the status of the room
        open_room["players"].append(display_name)
        open_room["status"] = "inprogress"
        self.pyre_db.child(self.game_branch).child(open_room_key).set(open_room)
        return open_room_key, open_room


    # FRIEND mode
    def create_friend_game(self, display_name: str, variant: str) -> (str, dict):
        return self.new_room([display_name], "friend", variant)


    def join_friend_game(self, display_name: str, game_id: str) -> (str, dict):
        db_query = self.pyre_db.child(self.game_branch).child(game_id).get()
        game_id, requested_room = db_query.key(), db_query.val()

        if not requested_room:
            raise RoomDoesNotExist
        if requested_room["mode"] != "friend":
            raise RoomIsNotFriend
        if requested_room["status"] == "inprogress":
            raise RoomIsInProgress

        requested_room["players"].append(display_name)
        requested_room["status"] = "inprogress"
        self.pyre_db.child(self.game_branch).child(game_id).set(requested_room)
        return game_id, requested_room
