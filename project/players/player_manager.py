'''
player_manager.py

objects and functions for managing player statistics

'''
import pdb
import pyrebase_ext

class PlayerManager:
    def __init__(self, db: pyrebase_ext.Database
                     , user_branch: str
                 ):
        '''
        constructor
        :param db: the firebase db
        :param user_branch: child name of where the users are stored
        '''
        self.db = db
        self.user_branch = user_branch

    # PYREBASE DOESN'T LET YOU SAVE CHAINED QUERIES INTO VARIABLES LOL
    def increment_stat(self, player_id: str, stat: str):
        current_stat = self.get_stat(player_id, stat)
        self.set_stat(player_id, stat, current_stat+1)


    def get_stat(self, player_id: str, stat: str):
        return self.db.child(self.user_branch).child(player_id).child(stat).get().val()

    def set_stat(self, player_id: str, stat: str, value):
        self.db.child(self.user_branch).child(player_id).child(stat).set(value)


    def add_win(self, player_id: str):
        self.increment_stat(player_id, "wins")

    def add_loss(self, player_id: str):
        self.increment_stat(player_id, "losses")

    def add_game_history(self, player_id: str, move_list: list):
        game_histories = self.get_stat(player_id, "gameHistories")

        if not game_histories:
            game_histories = [move_list]
        else:
            game_histories.append(move_list)

        self.set_stat(player_id, "gameHistories", game_histories)


    def remove_current_game(self, player_id: str, room_id: str):
        # get list of current games
        current_games = self.get_stat(player_id, "currentGames")

        current_games.remove(room_id)

        self.set_stat(player_id, "currentGames", current_games)
