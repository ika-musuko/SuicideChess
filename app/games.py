from app import pyre_db, firebase_login

### NEW GAME DATA ###
# make this dict the default data of a new game once the game data spec has been completed
# just replace it

class RoomDoesNotExist(Exception):
    pass

class RoomManager:
    def __init__(self, new_game_data):
        self.new_game_data = new_game_data


    # all these methods should return an (int, dict) tuple containing (game_id, room_data)
    def new_room(self, players: list, mode: str, variant: str) -> (int, dict):
        # get the latest game number and use as an ID
        total_games = pyre_db.child("TOTAL_GAMES").get().val()
        total_games += 1
        pyre_db.child("TOTAL_GAMES").set(total_games)

        # add a new game room
        room_data = {
              "gameId" : total_games
            , "players" : players
            , "currentPlayer" : 0
            , "variant" : variant
            , "status" : "waiting"
            , "gameData" : self.new_game_data
        }
        pyre_db.child(mode).child(total_games).set(room_data)
        return total_games, room_data

    # RANDOM mode
    def join_random_game(self, display_name: str, variant: str) -> (int, dict):
        open_room = pyre_db.child("random").order_by_child("status").equal_to("waiting").limit_to_first(1).get().val()
        if not open_room:
            return self.new_room([display_name], "random", variant)
        open_room["players"].append(display_name)
        open_room["status"] = "inprogress"
        pyre_db.child("random").child(open_room["gameId"]).set(open_room)
        return open_room["gameId"], open_room


    # FRIEND mode
    def create_friend_game(self, display_name: str, variant: str) -> (int, dict):
        return self.new_room([display_name], "friend", variant)


    def join_friend_game(self, display_name: str, game_id: int) -> (int, dict):
        requested_room = pyre_db.child("friend").child(game_id).get().val()
        if not requested_room:
            raise RoomDoesNotExist
        requested_room["players"].append(display_name)
        requested_room["status"] = "inprogress"
        pyre_db.child("friend").child(game_id).set(requested_room)
        return game_id, requested_room