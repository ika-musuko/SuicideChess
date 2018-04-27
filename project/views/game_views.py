'''
game_views.py

    routes for the game

'''

from flask_login import login_required, current_user
from flask import request, render_template, redirect, url_for, flash

from project import app, pyre_db, room_allocator
from project.views.view_utils import email_verified

from project.rooms import rooms

@app.route("/play/<room_id>")
@login_required
@email_verified
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
            _, room = room_allocator.get_room(room_id)
            return render_template("play.html", room_id=room_id, room=room)

        # handle errors
        except rooms.RoomDoesNotExist:
            flash("This room does not exist.")
            return redirect(url_for("index"))

    # user is not in the requested room
    flash("You are not playing in this room.")
    return redirect(url_for("index"))


@login_required
@email_verified
def add_to_current_games(room_id: str):
    # get the list of current games and add it to the user's
    # current game list
    current_games = current_user.get_db_property("currentGames")
    if current_games:
        current_games.append(room_id)
    else:
        current_games = [room_id]
    current_user.set_db_property("currentGames", current_games)


@app.route("/new_game/<variant>/<mode>")
@login_required
@email_verified
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
        room_id, requested_room = room_allocator.join_random_game(
              user_id=current_user.id
            , variant=variant
        )

        add_to_current_games(room_id)

        # go to the page with the new id
        return redirect(url_for("play", room_id=room_id))


    # friend mode (CREATING a new friend game)
    if mode == "friend":
        # create a new friend game
        room_id, requested_room = room_allocator.create_friend_game(
              user_id=current_user.id
            , variant=variant
        )

        add_to_current_games(room_id)

        # make a verification url for the friend game
        #verification_url = url_for("accept_friend_game", access_code=requested_room["accessCode"])
        return redirect(url_for("play", room_id=room_id))

    flash("This variant does not exist.")
    return redirect(url_for("index"))