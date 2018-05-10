'''
tests.py

!!!!! WARNING! DO NOT RUN THIS BY ITSELF! run run_tests.sh instead !!!!!

'''

# suppress ResourceWarning
import warnings

import unittest
import pdb
import os

from pyrebase_init import initialize_pyrebase

from project.rooms import room_exceptions
from project.models.new_game_data import NEW_GAME_DATA
from project.rooms import room_manager


class RoomTestCase(unittest.TestCase):

    def setUp(self):
        # suppress resource warnings
        warnings.simplefilter("ignore", ResourceWarning)

        # testing branch name
        self.testing_branch_name = "testing"

        # initialize the database
        self.pyre_db = initialize_pyrebase().database()

        # create games under the testing branch
        self.room_manager = room_manager.RoomManager(db=self.pyre_db, game_branch=self.testing_branch_name, new_game_data=NEW_GAME_DATA)

        # set player IDs
        self.player1 = "player1"
        self.player2 = "player2"


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
        self.room_manager.create_friend_game(
              user_id="the friend"
            , variant="tests"
        )

        # have players "a", "s", "d".... join random games
        for i, player in enumerate("asdfghjk"):
            #pdb.set_trace()
            # player joins a random game
            room_id, room = self.room_manager.join_random_game(user_id=player, variant="tests")


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
        id, _ = self.room_manager.create_friend_game(user_id=self.player1, variant="tests")
        db_query = self.pyre_db.child(self.testing_branch_name).child(id).get()
        game_id, requested_room = db_query.key(), db_query.val()

        # assert that the the room actually exists
        assert(requested_room)

        # assert that the only player in the room is the user who created the room
        assert(requested_room["players"] == [self.player1])

    def test_join_friend_game(self):
        '''
        case:
            join a friend game (valid)
        reason:
            when player joins a friend game normally, the player should be added to the list of players in that room
        traits:
            robustness, reusability

        '''
        room_id, room = self.room_manager.create_friend_game(user_id=self.player1, variant="tests")
        friend_room_id, room = self.room_manager.join_friend_game(user_id=self.player2, room_id=room_id, access_code=room["accessCode"])
        # make sure the friend's room id is the same as the one requested (same room)
        assert(room_id == friend_room_id)
        # make sure both players are in the room
        assert(self.player1 in room["players"] and self.player2 in room["players"])

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
        with self.assertRaises(room_exceptions.RoomDoesNotExist):
            self.room_manager.join_friend_game(user_id="coolman", room_id="nonexistentroom", access_code="")

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
        with self.assertRaises(room_exceptions.RoomIsNotWaiting):
            id, room = self.room_manager.create_friend_game(user_id=self.player1, variant="tests")
            id, room = self.room_manager.join_friend_game(user_id=self.player2, room_id=id, access_code=room["accessCode"])
            self.room_manager.join_friend_game(user_id="Barge Simpson", room_id=id, access_code=room["accessCode"])

    def test_join_friend_game_incorrect_access_code(self):
        '''
        case:
            make sure the access code is correct when joining a friend room

        return:
            throw an IncorrectAccessCode exception
        '''
        with self.assertRaises(room_exceptions.IncorrectAccessCode):
            id, room = self.room_manager.create_friend_game(user_id=self.player1, variant="tests")
            self.room_manager.join_friend_game(user_id=self.player2, room_id=id, access_code="WRONG!!!!!!")

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
        with self.assertRaises(room_exceptions.RoomIsNotFriend):
            id, room = self.room_manager.join_random_game(user_id="wowexcellentman", variant="tests")
            self.room_manager.join_friend_game(user_id="snooper", room_id=id, access_code="")

    def _create_new_game(self):
        # have two random users join games
        self.room_manager.join_random_game(user_id=self.player1, variant="tests")
        room_id, room = self.room_manager.join_random_game(user_id=self.player2, variant="tests")
        return room_id, room

    def test_rematch(self):
        '''
        case:
            rematch a room only under the prespecified conditions
        :return:
        '''
        room_id, room = self._create_new_game()

        # finish the game
        self.room_manager.set_room_status(room_id, "finished")

        # have one player rematch the room
        rematched_room_id, rematched_room = self.room_manager.rematch(room_id=room_id, current_user_id=self.player1)

        # make sure they are in the same room
        assert(rematched_room_id == room_id)

        # make sure only one player is ready and the other is not
        assert(rematched_room["rematchReady"][self.player1])
        assert(not rematched_room["rematchReady"][self.player2])

        # assert that the game is still "finished"
        assert(rematched_room["status"] == "finished")

        # have the other player rematch the room
        rematched_room_id, rematched_room = self.room_manager.rematch(room_id=room_id, current_user_id=self.player2)

        # make sure they are in the same room
        assert(rematched_room_id == room_id)

        # make sure room is reset
        assert(rematched_room["status"] == "inprogress")
        # make sure both players are in room
        assert(self.player1 in rematched_room["players"] and self.player2 in rematched_room["players"])
        # make sure both players' rematchReady state is set to False
        assert(not rematched_room["rematchReady"][self.player1] and not rematched_room["rematchReady"][self.player2])

        # try to rematch room without finishing it (should return rooms.RoomIsInProgress exception)
        with self.assertRaises(room_exceptions.RoomIsInProgress):
            self.room_manager.rematch(room_id=room_id, current_user_id=self.player1)


    def test_rematch_nonexistent(self):
        '''
        case:
            nonexistent rooms should not be able to rematch
        :return:
        '''
        # try to rematch a nonexistent room
        with self.assertRaises(room_exceptions.RoomDoesNotExist):
            self.room_manager.rematch(room_id="NONEXISTENT", current_user_id=self.player1)

    def test_rematch_room_in_progress(self):
        '''
        case:
            ensure that only finished games can be rematched

        :return:
        '''
        # create a new game
        room_id, room = self._create_new_game()

        # try to rematch room without finishing it (should return rooms.RoomIsInProgress exception)
        with self.assertRaises(room_exceptions.RoomIsInProgress):
            self.room_manager.rematch(room_id=room_id, current_user_id=self.player1)


    def test_rematch_non_player(self):
        '''
        case:
            ensure that only players in the game can rematch a game

        :return:
        '''
        # create a new game
        room_id, room = self._create_new_game()

        # finish the game
        self.room_manager.set_room_status(room_id, "finished")

        # have a non-player try to rematch the room
        with self.assertRaises(room_exceptions.RoomIsNotYours):
            self.room_manager.rematch(room_id=room_id, current_user_id="Barge Simpson")


    def test_clean_up_room(self):
        '''
        case:
            make sure the room doesn't exist after it is cleared
        :return:
        '''
        room_id, room = self._create_new_game()

        # clear the room
        self.room_manager.clean_up_room(room_id)

        with self.assertRaises(room_exceptions.RoomDoesNotExist):
            self.room_manager.get_room(room_id)

    def tearDown(self):
        self.pyre_db.child(self.testing_branch_name).remove()


if __name__ == "__main__":
    # run tests
    unittest.main()