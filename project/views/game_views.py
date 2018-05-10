'''
game_views.py

    routes for the game

'''

from functools import wraps

from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash

from project.rooms import room_exceptions
from project import app, room_manager, player_manager


@app.route("/play/<room_id>")
@login_required
def play(room_id: str):
    '''
    view for directly going to a room from an ID (like from the
    sidebar)
    :param room_id: the room ID
    :return: template for the room_id if the room exists and the
             player is in the room or redirect to home page with
             a flashed message.
    '''

    # check if the current user is in the requested room
    if room_id in current_user.get_db_property("currentGames"):
        try:
        # get the room from the room allocator
            _, room = room_manager.get_room(room_id)
            return render_template("play.html", room_id=room_id, room=room)

        # handle errors
        except room_exceptions.RoomDoesNotExist:
            flash("This room does not exist.")
            return redirect(url_for("index"))

    # handle if the room rematched (new room created)
    redirect_available = room_manager.redirect_available(room_id)
    if redirect_available:
        return redirect(url_for("play", room_id=redirect_available))

    # user is not in the requested room
    flash("You are not playing in this room.")
    return redirect(url_for("index"))


@app.route("/new_game/<variant>/<mode>")
@login_required
def new_game(variant: str, mode: str):
    '''
    view for creating a new game
    :param variant: the game variant eg: "blitz", "classic"
    :param mode: the game mode eg: "random", "friend"
    :return:
    '''
    # random mode
    if mode == "random":
        # join a random room
        room_id, requested_room = room_manager.join_random_game(
              user_id=current_user.id
            , variant=variant
        )

        # go to the page with the new id
        return redirect(url_for("play", room_id=room_id))


    # friend mode (CREATING a new friend game)
    if mode == "friend":
        # create a new friend game
        room_id, requested_room = room_manager.create_friend_game(
              user_id=current_user.id
            , variant=variant
        )

        # make a verification url for the friend game
        #verification_url = url_for("accept_friend_game", access_code=requested_room["accessCode"])
        return redirect(url_for("play", room_id=room_id))

    flash("This variant does not exist.")
    return redirect(url_for("index"))


@app.route("/invite/<room_id>/<access_code>")
@login_required
def invite(room_id: str, access_code: str):
    '''
    when a friend clicks on this link they will try to join the room
    it is successful if the access_code parameter matches the room's accessCode key
    :param room_id:
    :param access_code:
    :return:
    '''
    try:
        # try to join the room with the access code
        room_manager.join_friend_game(
              user_id=current_user.id
            , room_id=room_id
            , access_code=access_code
        )

        # go to the room
        return redirect(url_for("play", room_id=room_id))

    except room_exceptions.RoomDoesNotExist:
        flash("This room does not exist")
        return redirect(url_for("index"))
    except room_exceptions.RoomIsNotFriend:
        flash("This is not a friend room")
        return redirect(url_for("index"))
    except room_exceptions.IncorrectAccessCode:
        flash("Your invite URL is incorrect")
        return redirect(url_for("index"))
    except room_exceptions.RoomIsNotWaiting:
        flash("This room is not waiting for a friend")
        return redirect(url_for("index"))
    except room_exceptions.UserAlreadyInRoom:
        flash("You can't join your own room!")
        return redirect(url_for("play", room_id=room_id))


@app.route("/rematch/<room_id>")
@login_required
def rematch(room_id: str):
    '''
    rematch a game
    :param room_id:
    :return:
    '''

    # try to rematch the room
    try:
        rematched_room_id, _ = room_manager.rematch(room_id, current_user.id)

        # go back to the room
        return redirect(url_for("play", room_id=rematched_room_id))

    except room_exceptions.RoomDoesNotExist:
        flash("This room does not exist. Cannot rematch")
        return redirect(url_for("index"))
    except room_exceptions.RoomIsNotYours:
        flash("This room is not yours. You cannot rematch it.")
        return redirect(url_for("index"))
    except room_exceptions.RoomIsInProgress:
        flash("This room is still in progress")
        return redirect(url_for("play", room_id=room_id))
    except room_exceptions.RoomException:
        flash("This room does not exist anymore. Your room ID may have changed.")
        return redirect(url_for("index"))


@app.route("/exit_game/<room_id>")
@login_required
def exit_game(room_id: str):
    '''
    update the player statistics of the game and clean it up
    :param room_id:
    :return:
    '''
    try:
        # room["winner"] and room["moveList"] set by game app
        # update player statistics
        # check if the player is in the room
        if not room_manager.player_in_room(room_id, current_user.id):
            flash("You are not in this room.")
            return redirect(url_for("index"))

        _, room = room_manager.get_room(room_id)

        # update statistics for each player (win, loss, etc)
        if room["status"] != "waiting":
            player_manager.update_statistics(room_id, room)

        # remove the current game from the player's currentGames list
        for player in room["players"]:
            player_manager.remove_current_game(player, room_id)

        # clean up the game
        room_manager.clean_up_room(room_id)
        flash("thanks for playing!")

    except room_exceptions.RoomException:
        flash("This room does not exist anymore. Your room ID may have changed.")

    return redirect(url_for("index"))


@app.route("/simulate_game/<room_id>")
@login_required
def simulate_game(room_id: str):
    '''
    TEST GAME SIMULATOR
    :param room_id:
    :return:
    '''
    # get the room
    _, room = room_manager.get_room(room_id)

    ###########################
    ## ..................... ##
    ## ....play the game.... ##
    ## ..................... ##
    ###########################

    # game over, write to the room fields to be processed later
    room["status"] = "finished"
    room["winner"] = room["players"][0] # just get the first player as the winner for now
    room["moveList"] = ["wow", "this", "is", "a", "test"]
    room_manager.set_room(room_id, room)

    return redirect(url_for("play", room_id=room_id))

