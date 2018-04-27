'''
rooms.py

objects and functions for managing rooms.

'''


from project.models.new_room_data import new_room_data, new_friend_room_data
import pyrebase_ext

class UserAlreadyInRoom(Exception):
    '''
    raise this exception if a user is already in a room
    '''
    pass

class RoomDoesNotExist(Exception):
    '''
    raise this exception when a room does not exist
    '''
    pass

class RoomIsInProgress(Exception):
    '''
    raise this exception when a room is in progress
    '''
    pass

class RoomIsNotFriend(Exception):
    '''
    raise this exception when someone is trying to join a non-friend room using the join friend room interface
    '''
    pass

class RoomAllocator:
    """
    room allocator. responsible for allocating users to rooms and managing room states.

    rooms are basically dicts. see models/new_room_data.py for details
    """
    def __init__(self, db: pyrebase_ext.Database
                     , game_branch: str
                     , new_game_data: dict):
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

    # all these methods should return an (str, dict) tuple containing (game_id, room_data)
    def new_room(self, players: list
                     , mode: str
                     , variant: str
                     , status: str="waiting"
                     , friend_mode: bool=False
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
        ) if friend_mode else new_room_data(
                                    players
                                  , mode
                                  , variant
                                  , status
                                  , self.new_game_data)

        # update database
        self.db.child(self.game_branch)\
            .child(assigned_room_id).set(room_data)
        return assigned_room_id, room_data


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
        db_query = self.db.child(self.game_branch)\
            .order_by_child("mode").equal_to("random")\
            .order_by_child("status").equal_to("waiting")\
            .limit_to_first(2).get()
        branch, open_rooms = db_query.key(), db_query.val()

        # get the top room from the open rooms
        if open_rooms:
            open_room_key = next(iter(open_rooms))
            open_room = open_rooms[open_room_key]

        # if there are no open rooms, make a new room
        if not open_rooms or user_id in open_room["players"]:
            return self.new_room(
                  players=[user_id]
                , mode="random"
                , variant=variant
                , status="waiting"
            )


        # change the status of the room
        open_room["players"].append(user_id)
        open_room["status"] = "inprogress"
        self.db.child(self.game_branch)\
            .child(open_room_key).set(open_room)
        return open_room_key, open_room


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
        return self.new_room([user_id], "friend", variant, friend_mode=True)


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
                         , room_id: str) -> (str, dict):
        '''
        join an existing friend game
        :param user_id: the user who wants to join a friend game
        :param room_id: the room ID of the room the user wants to join
        :return: the room ID and the room itself in a tuple (the returned room ID should be the same as the one in the parameter)
        '''
        room_id, requested_room = self._query_room(room_id)

        if not requested_room:
            raise RoomDoesNotExist
        if requested_room["mode"] != "friend":
            raise RoomIsNotFriend
        if requested_room["status"] == "inprogress":
            raise RoomIsInProgress
        if user_id in requested_room["players"]:
            raise UserAlreadyInRoom

        requested_room["players"].append(user_id)
        requested_room["status"] = "inprogress"
        self.db.child(self.game_branch)\
            .child(room_id).set(requested_room)
        return room_id, requested_room

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

        # if the room does not exist in the database raise an exception
        if not requested_room:
            raise RoomDoesNotExist

        # return the room data
        return requested_room_id, requested_room

        # the room ID was not in the current user's room list so throw an exception


    def finish_room(self, room_id: str):
        '''
        delete the room from the room list
        !!! CALL THIS AFTER THE GAME STATISTICS HAVE BEEN RECORDED !!!
        :param room_id:
        :return:
        '''
        db_query = self.db.child(self.game_branch)\
            .child(room_id).get()
        db_query.remove()