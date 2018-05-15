"""
player_manager.py

objects and functions for managing player statistics

"""
import pyrebase_ext
from project.models.new_game_history import new_game_history
from project.players import player_exceptions


class PlayerManager:
    def __init__(self, db: pyrebase_ext.Database
                 , user_branch: str
                 ):
        """
        constructor
        :param db: the firebase db
        :param user_branch: child name of where the users are stored
        """
        self.db = db
        self.user_branch = user_branch

    # PYREBASE DOESN'T LET YOU SAVE CHAINED QUERIES INTO VARIABLES LOL
    def increment_stat(self, player_id: str, stat: str):
        current_stat = self.get_user_attribute(player_id, stat)
        self.set_user_attribute(player_id, stat, current_stat + 1)

    def get_user_attribute(self, player_id: str, stat: str):
        return self.db.child(self.user_branch).child(player_id).child(stat).get().val()

    def set_user_attribute(self, player_id: str, stat: str, value):
        self.db.child(self.user_branch).child(player_id).child(stat).set(value)

    def add_win(self, player_id: str):
        self.increment_stat(player_id, "wins")

    def add_draw(self, player_id: str):
        self.increment_stat(player_id, "draws")

    def add_loss(self, player_id: str):
        self.increment_stat(player_id, "losses")

    def add_game_history(self, player_id: str, room_id: str, game_history: dict):
        game_histories = self.get_user_attribute(player_id, "gameHistories")

        if not game_histories:
            game_histories = {room_id: game_history}
        else:
            game_histories[room_id] = game_history

        self.set_user_attribute(player_id, "gameHistories", game_histories)

    def remove_current_game(self, player_id: str, room_id: str):
        # get list of current games
        current_games = self.get_user_attribute(player_id, "currentGames")

        current_games.remove(room_id)

        self.set_user_attribute(player_id, "currentGames", current_games)

    def update_statistics(self, room_id: str, room: dict):
        for player in room["players"]:
            # add the current room's move list to the game history
            game_history = new_game_history(
                move_list=room["moveList"]
                , winner=room["winner"]
            )
            self.add_game_history(player, room_id, game_history)

            if not room["winner"] or room["winner"] == "$DUMMY":
                self.add_draw(player)

            # add a win for the winner
            elif player == room["winner"]:
                self.add_win(player)

            # else add a loss for the loser
            else:
                self.add_loss(player)

    def add_current_game(self, player_id: str, room_id: str):
        # get the list of current games and add it to the user's
        # current game list
        current_games = self.get_user_attribute(player_id, "currentGames")

        if current_games:
            # don't add a duplicate game
            if room_id in current_games:
                return

            current_games.append(room_id)
        else:
            current_games = [room_id]

        self.set_user_attribute(player_id, "currentGames", current_games)

    def get_user(self, user_id: str) -> dict:
        # try to get a user
        user = self.db.child(self.user_branch).child(user_id).get().val()
        if not user:
            raise player_exceptions.PlayerNotFound
        return user

    def get_display_name(self, player_id: str) -> str:
        """
        get the display name from a player
        :param player_id:
        :return:
        """
        return self.get_user_attribute(player_id, "displayName")

    def get_all_user_ids(self) -> list:
        """
        return every user id
        :return:
        """
        all_user_data = self.db.child(self.user_branch).get().val()
        return all_user_data.keys() if all_user_data else []
