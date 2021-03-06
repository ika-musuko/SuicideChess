"""
new_user_data.py

    the data structure for a new user.
"""
import datetime

def new_user_data(display_name: str, e_mail: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "displayName": display_name
        , "draws": 0
        , "email": e_mail
        , "emailNotifications": True
        , "currentGames": []  # store the game IDs to the games the user is currently in here
        , "gameHistories": []  # store the full game data of any past games for a player in here
        , "losses": 0
        , "rank": 0
        , "wins": 0
        , "bio": "This user has not written a bio yet."
        , "joinedOn" : now
        , "lastHere" : now
    }
