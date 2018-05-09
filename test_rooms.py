import unittest
import pdb
import os

from project import app, pyre_db
from project.models.new_game_data import NEW_GAME_DATA
from project.rooms.rooms import RoomManager, RoomDoesNotExist, RoomIsInProgress, RoomIsNotFriend, RoomIsNotYours

class RoomTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        # create games under the testing branch
        self.rm_test = RoomManager(pyre_db, "testing", NEW_GAME_DATA)
        self.player1 = "a"
        self.player2 = "g"

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

        # create a friend room
        self.rm_test.create_friend_game(
              user_id="the friend"
            , variant="tests"
        )

        # have players "a", "s", "d".... join random games
        for i, player in enumerate("asdfghjk"):
            #pdb.set_trace()
            # player joins a random game
            room_id, room = self.rm_test.join_random_game(user_id=player, variant="tests")


            # ensure this is a random room
            assert(room["mode"] == "random")

            # if the 'index' of the player list is even, then that means the player made a new game and it is "waiting"
            if i % 2 == 0:
                assert(
                       room["status"] == "waiting"
                       and len(room["players"]) == 1
                       and room["players"] == [player]
                )

            # else, the player joined an existing game. ensure that the game is "inprogress" and the players list contains both players
            else:
                #pdb.set_trace()
                assert(
                       room["status"] == "inprogress"
                       and len(room["players"]) == 2
                       and player in room["players"]
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

    def _create_new_game(self):
        # have two random users join games
        self.rm_test.join_random_game(user_id=self.player1, variant="tests")
        room_id, room = self.rm_test.join_random_game(user_id=self.player1, variant="tests")
        return room_id, room

    def test_rematch(self):
        '''
        case:
            rematch a room only under the prespecified conditions
        :return:
        '''
        room_id, room = self._create_new_game()

        # finish the game
        self.rm_test.set_room_status(room_id, "finished")

        # have one player rematch the room
        rematched_room_id, rematched_room = self.rm_test.rematch(room_id=room_id, current_user_id=self.player1)

        # make sure they are in the same room
        assert(rematched_room_id == room_id)

        # make sure only one player is ready and the other is not
        assert(rematched_room["rematchReady"][self.player1])
        assert(not rematched_room["rematchReady"][self.player2])

        # assert that the game is still "finished"
        assert(rematched_room["status"] == "finished")

        # have the other player rematch the room
        rematched_room_id, rematched_room = self.rm_test.rematch(room_id=room_id, current_user_id=self.player2)

        # make sure they are in the same room
        assert(rematched_room_id == room_id)

        # make sure room is reset
        assert(rematched_room["status"] == "inprogress")
        # make sure both players are in room
        assert(self.player1 in rematched_room["players"] and self.player2 in rematched_room["players"])
        # make sure both players' rematchReady state is set to False
        assert(not rematched_room["rematchReady"][self.player1] and not rematched_room["rematchReady"][self.player2])

        # try to rematch room without finishing it (should return RoomIsInProgress exception)
        with self.assertRaises(RoomIsInProgress):
            self.rm_test.rematch(room_id=room_id, current_user_id=self.player1)


    def test_rematch_nonexistent(self):
        '''
        case:
            nonexistent rooms should not be able to rematch
        :return:
        '''
        # try to rematch a nonexistent room
        with self.assertRaises(RoomDoesNotExist):
            self.rm_test.rematch(room_id="NONEXISTENT", current_user_id=self.player1)

    def test_rematch_room_in_progress(self):
        '''
        case:
            ensure that only finished games can be rematched

        :return:
        '''
        # create a new game
        room_id, room = self._create_new_game()

        # try to rematch room without finishing it (should return RoomIsInProgress exception)
        with self.assertRaises(RoomIsInProgress):
            self.rm_test.rematch(room_id=room_id, current_user_id=self.player1)


    def test_rematch_non_player(self):
        '''
        case:
            ensure that only players in the game can rematch a game

        :return:
        '''
        # create a new game
        room_id, room = self._create_new_game()

        # finish the game
        self.rm_test.set_room_status(room_id, "finished")

        # have a non-player try to rematch the room
        with self.assertRaises(RoomIsNotYours):
            self.rm_test.rematch(room_id=room_id, current_user_id="Barge Simpson")



    def tearDown(self):
        pyre_db.child("testing").remove()


if __name__ == "__main__":
    unittest.main()