import unittest

from app import app, pyre_db
from app.new_game_data import NEW_GAME_DATA
from app.rooms import RoomManager, RoomDoesNotExist, RoomIsInProgress, RoomIsNotFriend


class RoomTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.rm_test = RoomManager(pyre_db,"testing", NEW_GAME_DATA)

    def test_join_random_game(self):
        for i, c in enumerate("asdfghjk"):
            id, room = self.rm_test.join_random_game(user_id=c, variant="test")
            if i % 2 == 0:
                assert(room["status"] == "waiting")
            else:
                assert(room["status"] == "inprogress")

    def test_create_friend_game(self):
        id, _ = self.rm_test.create_friend_game(user_id="user1", variant="test")
        db_query = pyre_db.child("testing").child(id).get()
        game_id, requested_room = db_query.key(), db_query.val()
        assert(requested_room)
        assert(requested_room["players"][0] == "user1")

    def test_join_friend_game(self):
        room_id, _ = self.rm_test.create_friend_game(user_id="user1", variant="test")
        friend_room_id, room = self.rm_test.join_friend_game(user_id="user2", game_id=room_id)
        assert(room_id == friend_room_id)
        assert("user1" in room["players"] and "user2" in room["players"])

    def test_join_friend_game_not_exist(self):
        with self.assertRaises(RoomDoesNotExist):
            self.rm_test.join_friend_game(user_id="coolman", game_id="nonexistentroom")

    def test_join_friend_game_in_progress(self):
        with self.assertRaises(RoomIsInProgress):
            id, _ = self.rm_test.create_friend_game(user_id="user1", variant="test")
            friend_id, _ = self.rm_test.join_friend_game(user_id="user2", game_id=id)
            self.rm_test.join_friend_game(user_id="Barge Simpson", game_id=id)

    def test_join_friend_game_not_friend(self):
        with self.assertRaises(RoomIsNotFriend):
            id, _ = self.rm_test.join_random_game(user_id="wowexcellentman", variant="test")
            self.rm_test.join_friend_game(user_id="snooper", game_id=id)

    def tearDown(self):
        pyre_db.child("testing").remove()


if __name__ == "__main__":
    unittest.main()