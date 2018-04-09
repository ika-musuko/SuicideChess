from app import pyre_db, firebase_login

class GameDoesNotExist(Exception):
    pass

def new_room(players: list, mode: str, variant: str, game_data: dict) -> int:
    # get the latest game number and use as an ID
    total_games = pyre_db.child("TOTAL_GAMES").get().val()
    total_games += 1
    pyre_db.child("TOTAL_GAMES").set(total_games)

    # add a new game room
    game_room_data = {
          "players" : players
        , "currentPlayer" : 0
        , "variant" : variant
        , "status" : "waiting"
        , "gameData" : game_data
    }
    pyre_db.child(mode).child(total_games).set(game_room_data)
    return total_games

def friend_join_game(display_name: str, game_id: int) -> dict:
    requested_game = pyre_db.child("friend").child(game_id).get().val()
    if not requested_game:
        raise GameDoesNotExist
    requested_game["players"].append(display_name)
    requested_game["status"] = "inprogress"
    pyre_db.child("friend").child(game_id).set(requested_game)
    return requested_game