import datetime


def new_game_history(move_list: list, winner: str) -> dict:
    return {
        "timeFinished": str(datetime.datetime.today())  # string of the time finished
        , "moveList": move_list  # list of the moves
        , "winner": winner
    }
