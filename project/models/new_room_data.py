'''
new_room_data.py

    the data structure for a new room it's just a dict so we can store it on firebase easily
'''

from random import randint

def new_room_data(players: list, mode: str, variant: str, status: str, new_game_data: dict):
    return        {
                  "players" : players
                , "mode"   : mode
                , "variant" : variant
                , "status" : status
                , "gameData" : new_game_data
                , "rematchReady" : {player: False for player in players}

                , "winner" : "" # GAME APP output
                , "moveList" : [] # GAME APP output
            }

def new_friend_room_data(players: list, mode: str, variant: str, status: str, new_game_data: dict):
    new_room = new_room_data(players, mode, variant, status, new_game_data)
    new_room['accessCode'] = str(randint(0, 2**128))
    return new_room