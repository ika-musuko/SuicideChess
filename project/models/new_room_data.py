def new_room_data(players: list, mode: str, variant: str, status: str, new_game_data: dict):
    return        {
                  "players" : players
                , "mode"   : mode
                , "variant" : variant
                , "status" : status
                , "gameData" : new_game_data
            }