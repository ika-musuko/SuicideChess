'''
room_manager.py

objects and functions for managing rooms.

'''

import pdb
from project.models.new_room_data import new_room_data, new_friend_room_data
from project.rooms import room_exceptions
from project.players.player_manager import PlayerManager
import pyrebase_ext


class RoomManager:
    """
    room manager. responsible for allocating users to rooms and managing room states.

    rooms are basically dicts. see models/new_room_data.py for details
    """
    def __init__(self, db: pyrebase_ext.Database
                 , game_branch: str
                 , new_game_data: dict
                 , rematch_redirects_branch: str
                 , player_manager: PlayerManager=None):
        '''
        constructor
        :param db: the firebase db
        :param game_branch: the name of the parent node to store
                            all the rooms. for our thing it'll be
                            "suicide_chess" but for tests we can use
                            "testing". if we were to make more games, t
                             this is where the name
                            of those games would be placed
        :param new_game_data: the default data for a new game
        '''
        self.db = db
        self.game_branch = game_branch
        self.new_game_data = new_game_data
        self.rematch_redirects_branch = rematch_redirects_branch
        self.player_manager = player_manager


    # all these methods should return an (str, dict) tuple containing (game_id, room_data)
    def _new_room(self, players: list
                  , mode: str
                  , variant: str
                  , status: str="waiting"
                  ) -> (str, dict):
        '''
        create a new room
        :param players: the list of players for the new room
        :param mode: the game mode (ex: 'friend', 'random')
        :param variant: the game variant (ex: 'blitz', 'classic')
        :param status: is the game waiting or
                       inprogress or finished?
        :return: the room ID and the room itself in a tuple
        '''
        # get the latest game number and use as an ID
        total_games = self.db.child(self.game_branch)\
            .child("TOTAL_GAMES").get().val()
        if not total_games:
            self.db.child(self.game_branch)\
                .child("TOTAL_GAMES").set(0)
            total_games = 0
        total_games += 1
        self.db.child(self.game_branch)\
            .child("TOTAL_GAMES").set(total_games)
        assigned_room_id = "%s%s%s" % (variant, mode, total_games)

        # add a new game room
        room_data = new_friend_room_data(
                                    players
                                  , mode
                                  , variant
                                  , status
                                  , self.new_game_data
        ) if mode == "friend" else new_room_data(
                                    players
                                  , mode
                                  , variant
                                  , status
                                  , self.new_game_data)

        # update database
        self.db.child(self.game_branch)\
            .child(assigned_room_id).set(room_data)
        return assigned_room_id, room_data


    def add_player(self, room_id: str, user_id: str, room: dict=None) -> (str, dict):
        # get the room if it is not already provided in the parameter
        if not room:
            _, room = self.get_room(room_id)

        # add to user's current game list
        if self.player_manager:
            self.player_manager.add_current_game(user_id, room_id)

        # if the player list is empty, create a new list
        if not room["players"]:
            room["players"] = [user_id]

        # otherwise append this player to the list
        elif user_id not in room["players"]:
            room["players"].append(user_id)

        # this player is not "ready to rematch"
        room["rematchReady"][user_id] = False


        # set the room data
        return self.set_room(room_id, room)

    # RANDOM mode
    def join_random_game(self
                         , user_id: str
                         , variant: str) -> (str, dict):
        '''
        have a user join a random game
        :param user_id: the ID of the user joining
        :param variant: which variant to play
        :return: the room ID and the room itself in a tuple
        '''
        # firebase only lets you filter on one condition epic fail
        '''
        db_query = self.db.child(self.game_branch)\
            .order_by_child("mode").equal_to("random")\
            .order_by_child("status").equal_to("waiting")\
            .limit_to_first(2).get()
        '''
        def create_new_random_game():

            room_id, room = self._new_room(
                players=[user_id]
                , mode="random"
                , variant=variant
                , status="waiting"
            )
            return self.add_player(room_id, user_id)

        # get all the random games
        db_query = self.db.child(self.game_branch)\
            .order_by_child("mode").equal_to("random")\
            .get()

        branch, random_rooms = db_query.key(), db_query.val()
        if not random_rooms:
            return create_new_random_game()

        # get the first random waiting game (open room)
        for room_name in random_rooms:
            if random_rooms[room_name]["status"] == "waiting":
                open_room_id, open_room = room_name, random_rooms[room_name]
                break
        else:
            return create_new_random_game()

        # if the player himself is in the room, create a new random game
        # players can't play themselves!
        if user_id in open_room["players"]:
            return create_new_random_game()


        ## A VALID ROOM EXISTS so join it
        # change the status of the room
        open_room["status"] = "inprogress"

        # add the player to the room
        return self.add_player(open_room_id, user_id, open_room)



    def set_room(self, room_id: str, room: dict) -> (str, dict):
        # check if the room exists
        self.get_room(room_id)

        # set the room
        self.db.child(self.game_branch) \
            .child(room_id).set(room)

        # set the room status
        return self.set_room_status(room_id, room["status"])

    def set_room_status(self, room_id: str, status: str) -> (str, dict):
        _, room = self.get_room(room_id)
        self._set_room_attribute(
              room_id=room_id
            , attribute="status"
            , value=status
        )

        if status == "inprogress":
            self._set_room_attribute(
                  room_id=room_id
                , attribute="rematchReady"
                , value={player: False for player in room["players"]}
            )

        _, room = self.get_room(room_id)
        return room_id, room

    # FRIEND mode
    def create_friend_game(self
                           , user_id: str
                           , variant: str) -> (str, dict):
        '''
        create a new friend game
        :param user_id: the user who wants to create the game
        :param variant: the variant of the game
        :return: the room ID and the room itself in a tuple
        '''
        room_id, room = self._new_room([user_id], "friend", variant)
        return self.add_player(room_id, user_id)

    def _query_room(self
                    , room_id: str) -> (str, dict):
        '''
        helper method for querying a single room from a room id
        :param room_id: the room id
        :return: the room id and the room itself in a tuple
        '''
        db_query = self.db.child(self.game_branch)\
            .child(room_id).get()
        return db_query.key(), db_query.val()

    def join_friend_game(self
                         , user_id: str
                         , room_id: str
                         , access_code: str) -> (str, dict):
        '''
        join an existing friend game
        :param user_id: the user who wants to join a friend game
        :param room_id: the room ID of the room the user wants to join
        :return: the room ID and the room itself in a tuple (the returned room ID should be the same as the one in the parameter)
        '''
        room_id, requested_room = self._query_room(room_id)

        # make sure the room exists
        if not requested_room:
            raise room_exceptions.RoomDoesNotExist
        # make sure the room is a friend room
        if requested_room["mode"] != "friend":
            raise room_exceptions.RoomIsNotFriend
        # make sure the access code is correct
        if requested_room["accessCode"] != access_code:
            raise room_exceptions.IncorrectAccessCode
        # make sure the game is not already in progress
        if requested_room["status"] != "waiting":
            raise room_exceptions.RoomIsNotWaiting
        # make sure the player is not trying to join his own room
        if user_id in requested_room["players"]:
            raise room_exceptions.UserAlreadyInRoom

        ## IF ALL THE ABOVE TESTS FALL THROUGH the join was successful
        # update the room status
        requested_room["status"] = "inprogress"

        # add player to the room
        return self.add_player(room_id, user_id, requested_room)


    def get_room(self, room_id: str) -> (str, dict):
        '''
        go to a room from the room id
        this will only return a room if the player has
        this room in their current game list
        :param user:
        :param room_id:
        :return:
        '''
        requested_room_id, requested_room = \
            self._query_room(room_id)

        # if the room does not exist in the database raise room_exceptions.an exception
        if not requested_room:
            raise room_exceptions.RoomDoesNotExist

        # return the room data
        return requested_room_id, requested_room



    def set_room_attribute(self, room_id: str, attribute: str, value):
        # don't use this to set room["status"]
        if attribute == "status":
            raise room_exceptions.UseSetRoomStatus

        self._set_room_attribute(room_id, attribute, value)

    def _set_room_attribute(self, room_id: str, attribute: str, value):
        # check if the room exists (this should throw a RoomDoesNotExist exception if it doesn't exist)
        self.get_room(room_id)

        # set the attribute
        self.db.child(self.game_branch).child(room_id).child(attribute).set(value)

    def clean_up_room(self, room_id: str):
        '''
        delete the room from the room list
        !!! CALL THIS AFTER THE GAME STATISTICS HAVE BEEN RECORDED !!!
        :param room_id:
        :return:
        '''
        db_query = self.db.child(self.game_branch)\
            .child(room_id).remove()

    def reset_room(self, room_id: str):
        '''
        boot the players out of the current room and put them in a new room
        :param room_id:
        :return:
        '''
        # get the room
        _, room = self.get_room(room_id)

        # delete the current room from the database
        self.clean_up_room(room_id)

        # make a new room for the players
        new_room_id, new_room = self._new_room(
                              players=room["players"]
                            , mode=room["mode"]
                            , variant=room["variant"]
                        )

        # set the redirect path
        self.db.child(self.rematch_redirects_branch).child(room_id).set(new_room_id)

        # delete the game from each player's current games and add the new room
        if self.player_manager:
            for player in room["players"]:
                self.player_manager.remove_current_game(player, room_id)
                self.player_manager.add_current_game(player, new_room_id)

        # update database
        new_room["status"] = "inprogress"
        return self.set_room(new_room_id, new_room)


    def rematch(self, room_id: str, current_user_id: str) -> (str, dict):
        # get the room data from the room allocator
        requested_room_id, room = self.get_room(room_id)

        # blow out to index if the room doesn't exist
        if not room:
            raise room_exceptions.RoomDoesNotExist

        # make sure the current user is in the room he's trying to rematch
        if current_user_id not in room["players"]:
            raise room_exceptions.RoomIsNotYours

        # if the room is in progress, notify the player they cannot rematch until the game finishes
        if room["status"] != "finished":
            raise room_exceptions.RoomIsInProgress

        # actually try to rematch the game
        room["rematchReady"][current_user_id] = True

        # if all of the players are ready
        if all(ready_state for ready_state in room["rematchReady"].values()):
            # reset the room
            if self.player_manager:
                self.player_manager.update_statistics(room_id, room)
            return self.reset_room(room_id)

        return self.set_room(room_id, room)


    def get_status(self, room_id: str) -> str:
        _, room = self.get_room(room_id)
        return room["status"]

    def player_in_room(self, room_id: str, user_id) -> bool:
        '''
        check if a player is in the room
        :param room_id:
        :param user_id:
        :return:
        '''
        _, room = self.get_room(room_id)
        return user_id in room["players"]


    def get_players_by_id(self, room_id: str) -> list:
        '''
        return the list of players in the room by display name
        :param room_id:
        :return:
        '''
        _, room = self.get_room(room_id)
        return room["players"] if room["players"] else []


    def get_players_by_display_name(self, room_id: str) -> list:
        '''
        return the list of players in the room by display name
        :param room_id:
        :return:
        '''
        _, room = self.get_room(room_id)

        # just return the player usernames if the player manager has not been initialized
        if not self.player_manager:
            return room["players"]

        # convert the user ID list into a display name list
        return [self.player_manager.get_display_name(player) for player in room["players"]]


    def redirect_available(self, room_id: str):
        '''
        check if this room redirects to another room
        :param room_id:
        :return:
        '''
        return self.db.child(self.rematch_redirects_branch).child(room_id).get().val()