"""
new_room_data.py

    the data structure for a new room it's just a dict so we can store it on firebase easily
"""

import random
import string


def generate_access_code() -> str:
    """
    generate an alphanumeric access code for friend rooms
    :return:
    """
    character_pool = ''.join((string.ascii_letters, string.digits))
    return ''.join(random.choice(character_pool) for _ in range(8))


def new_room_data(players: list, mode: str, variant: str, status: str, new_game_data: dict):
    return {
        "players": players
        , "mode": mode
        , "variant": variant
        , "status": status
        , "gameData": new_game_data
        , "rematchReady": {player: False for player in players}

        , "winner": ""  # GAME APP output
        , "gameHistory": {}  # GAME APP output
    }


def new_friend_room_data(players: list, mode: str, variant: str, status: str, new_game_data: dict):
    new_room = new_room_data(players, mode, variant, status, new_game_data)
    new_room['accessCode'] = generate_access_code()
    return new_room
