import unittest
import pdb

from project import app, pyre_db
from project.models.new_game_data import NEW_GAME_DATA
from project.rooms.rooms import RoomAllocator, RoomDoesNotExist, RoomIsInProgress, RoomIsNotFriend

class RoomTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        # create games under the testing branch
        self.rm_test = RoomAllocator(pyre_db, "testing", NEW_GAME_DATA)

    def test_join_random_game(self):
        '''
        case:
            joining random games
        reason:
            when players join a random game, they should join an existing waiting game or create a new one if no
            waiting games exist
        traits:
            robustness, reusability

        '''

        # have players "a", "s", "d".... join random games
        for i, player in enumerate("asdfghjk"):
            pdb.set_trace()
            # player joins a random game
            player_id, room = self.rm_test.join_random_game(user_id=player, variant="tests")

            # if the 'index' of the player list is even, then that means the player made a new game and it is "waiting"
            if i % 2 == 0:
                assert(
                       room["status"] == "waiting"
                       and len(room["players"]) == 1
                       and room["players"] == [player_id]
                )

            # else, the player joined an existing game. ensure that the game is "inprogress" and the players list contains both players
            else:
                assert(
                       room["status"] == "inprogress"
                       and len(room["players"]) == 2
                       and player_id in room["players"]
                )

    def test_create_friend_game(self):
        '''
        case:
            creating a new friend game
        reason:
            when a user creates a new friend game, they should join that game and wait
        traits:
            robustness, reusability

        '''
        id, _ = self.rm_test.create_friend_game(user_id="user1", variant="tests")
        db_query = pyre_db.child("testing").child(id).get()
        game_id, requested_room = db_query.key(), db_query.val()

        # assert that the the room actually exists
        assert(requested_room)

        # assert that the only player in the room is the user who created the room
        assert(requested_room["players"] == ["user1"])

    def test_join_friend_game(self):
        '''
        case:
            join a friend game (valid)
        reason:
            when player joins a friend game normally, the player should be added to the list of players in that room
        traits:
            robustness, reusability

        '''
        room_id, _ = self.rm_test.create_friend_game(user_id="user1", variant="tests")
        friend_room_id, room = self.rm_test.join_friend_game(user_id="user2", room_id=room_id)
        # make sure the friend's room id is the same as the one requested (same room)
        assert(room_id == friend_room_id)
        # make sure both players are in the room
        assert("user1" in room["players"] and "user2" in room["players"])

    def test_join_friend_game_not_exist(self):
        '''
        case:
            joining a friend game (room doesn't exist)
        reason:
            when a player tries to join a friend game that doesn't exist, tell the user that the room doesn't exist
        traits:
            robustness, reusability

        '''
        # throw exception signaling that the room doesn't exist
        with self.assertRaises(RoomDoesNotExist):
            self.rm_test.join_friend_game(user_id="coolman", room_id="nonexistentroom")

    def test_join_friend_game_in_progress(self):
        '''
        case:
            joining a friend game (room already has two people)
        reason:
            when a player tries to join a friend game that already has two people, they should not be allowed to join
        traits:
            robustness, reusability

        '''
        # throw exception signaling that the room is full
        with self.assertRaises(RoomIsInProgress):
            id, _ = self.rm_test.create_friend_game(user_id="user1", variant="tests")
            friend_id, _ = self.rm_test.join_friend_game(user_id="user2", room_id=id)
            self.rm_test.join_friend_game(user_id="Barge Simpson", room_id=id)

    def test_join_friend_game_not_friend(self):
        '''
        case:
            joining a friend game (room is not a friend room)
        reason:
            when players join a random game, they should join an existing waiting game or create a new one if no
            waiting games exist
        traits:
            robustness, reusability

        '''
        with self.assertRaises(RoomIsNotFriend):
            id, _ = self.rm_test.join_random_game(user_id="wowexcellentman", variant="tests")
            self.rm_test.join_friend_game(user_id="snooper", room_id=id)

    def tearDown(self):
        pyre_db.child("testing").remove()


if __name__ == "__main__":
    unittest.main()