'''
rooms.py

objects and functions for managing rooms.

'''


from project.models.new_room_data import new_room_data
import pyrebase_ext


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
    def __init__(self, db: pyrebase_ext.Database, game_branch: str, new_game_data: dict):
        '''
        constructor
        :param db: the firebase db
        :param game_branch: the name of the parent node to store all the rooms. for our thing it'll be "suicide_chess"
                            but for tests we can use "testing". if we were to make more games, this is where the name
                            of those games would be placed
        :param new_game_data: the default data for a new game
        '''
        self.db = db
        self.game_branch = game_branch
        self.new_game_data = new_game_data

    # all these methods should return an (str, dict) tuple containing (game_id, room_data)
    def new_room(self, players: list, mode: str, variant: str, status: str="waiting") -> (str, dict):
        '''
        create a new room
        :param players: the list of players for the new room
        :param mode: the game mode (ex: 'friend', 'random')
        :param variant: the game variant (ex: 'blitz', 'classic')
        :param status: is the game waiting or inprogress or finished?
        :return: the room ID and the room itself in a tuple
        '''
        # get the latest game number and use as an ID
        total_games = self.db.child(self.game_branch).child("TOTAL_GAMES").get().val()
        if not total_games:
            self.db.child(self.game_branch).child("TOTAL_GAMES").set(0)
            total_games = 0
        total_games += 1
        self.db.child(self.game_branch).child("TOTAL_GAMES").set(total_games)
        assigned_room_id = "Room%s" % total_games

        # add a new game room
        room_data = new_room_data(players, mode, variant, status, self.new_game_data)
        self.db.child(self.game_branch).child(assigned_room_id).set(room_data)
        return assigned_room_id, room_data


    # RANDOM mode
    def join_random_game(self, user_id: str, variant: str) -> (str, dict):
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

        # if there are no open rooms, make a new room
        if not open_rooms:
            return self.new_room([user_id], "random", variant)

        # get the top room from the open rooms
        open_room_key = next(iter(open_rooms))
        open_room = open_rooms[open_room_key]

        # change the status of the room
        open_room["players"].append(user_id)
        open_room["status"] = "inprogress"
        self.db.child(self.game_branch).child(open_room_key).set(open_room)
        return open_room_key, open_room


    # FRIEND mode
    def create_friend_game(self, user_id: str, variant: str) -> (str, dict):
        '''
        create a new friend game
        :param user_id: the user who wants to create the game
        :param variant: the variant of the game
        :return: the room ID and the room itself in a tuple
        '''
        return self.new_room([user_id], "friend", variant)


    def join_friend_game(self, user_id: str, room_id: str) -> (str, dict):
        '''
        join an existing friend game
        :param user_id: the user who wants to join a friend game
        :param room_id: the room ID of the room the user wants to join
        :return: the room ID and the room itself in a tuple (the returned room ID should be the same as the one in the parameter)
        '''
        db_query = self.db.child(self.game_branch).child(room_id).get()
        room_id, requested_room = db_query.key(), db_query.val()

        if not requested_room:
            raise RoomDoesNotExist
        if requested_room["mode"] != "friend":
            raise RoomIsNotFriend
        if requested_room["status"] == "inprogress":
            raise RoomIsInProgress

        requested_room["players"].append(user_id)
        requested_room["status"] = "inprogress"
        self.db.child(self.game_branch).child(room_id).set(requested_room)
        return room_id, requested_room
