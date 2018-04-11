import unittest

from project import app, pyre_db
from project.models.new_game_data import NEW_GAME_DATA
from project.rooms import RoomManager, RoomDoesNotExist, RoomIsInProgress, RoomIsNotFriend

class RoomTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        # create games under the testing branch
        self.rm_test = RoomManager(pyre_db,"testing", NEW_GAME_DATA)

    def test_join_random_game(self):
        '''
        case:
            joining random games
        reason:
            when players join a random game, they should join an existing waiting game or create a new one if none exist
        traits:

        '''

        # have players "a", "s", "d".... join random games
        for i, player in enumerate("asdfghjk"):

            # player joins a random game
            id, room = self.rm_test.join_random_game(user_id=player, variant="tests")

            # if the 'index' of the player list is even, then that means the player made a new game and it is "waiting"
            if i % 2 == 0:
                assert(room["status"] == "waiting")

            # else, the player joined an existing game. ensure that the game is "inprogress" and the players list contains both players
            else:
                assert(room["status"] == "inprogress" and len(room["players"]) > 1)

    def test_create_friend_game(self):
        id, _ = self.rm_test.create_friend_game(user_id="user1", variant="tests")
        db_query = pyre_db.child("testing").child(id).get()
        game_id, requested_room = db_query.key(), db_query.val()
        assert(requested_room)
        assert(requested_room["players"] == ["user1"])

    def test_join_friend_game(self):
        room_id, _ = self.rm_test.create_friend_game(user_id="user1", variant="tests")
        friend_room_id, room = self.rm_test.join_friend_game(user_id="user2", room_id=room_id)
        assert(room_id == friend_room_id)
        assert("user1" in room["players"] and "user2" in room["players"])

    def test_join_friend_game_not_exist(self):
        with self.assertRaises(RoomDoesNotExist):
            self.rm_test.join_friend_game(user_id="coolman", room_id="nonexistentroom")

    def test_join_friend_game_in_progress(self):
        with self.assertRaises(RoomIsInProgress):
            id, _ = self.rm_test.create_friend_game(user_id="user1", variant="tests")
            friend_id, _ = self.rm_test.join_friend_game(user_id="user2", room_id=id)
            self.rm_test.join_friend_game(user_id="Barge Simpson", room_id=id)

    def test_join_friend_game_not_friend(self):
        with self.assertRaises(RoomIsNotFriend):
            id, _ = self.rm_test.join_random_game(user_id="wowexcellentman", variant="tests")
            self.rm_test.join_friend_game(user_id="snooper", room_id=id)

    def tearDown(self):
        pyre_db.child("testing").remove()


if __name__ == "__main__":
    unittest.main()