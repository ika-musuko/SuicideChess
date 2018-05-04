'''
game_views.py

    routes for the game

'''

from flask_login import login_required, current_user
from flask import request, render_template, redirect, url_for, flash

from project import app, pyre_db, room_manager
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
            _, room = room_manager.get_room(room_id)
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
        room_id, requested_room = room_manager.join_random_game(
              user_id=current_user.id
            , variant=variant
        )

        print(requested_room["mode"])

        add_to_current_games(room_id)

        # go to the page with the new id
        return redirect(url_for("play", room_id=room_id))


    # friend mode (CREATING a new friend game)
    if mode == "friend":
        # create a new friend game
        room_id, requested_room = room_manager.create_friend_game(
              user_id=current_user.id
            , variant=variant
        )

        add_to_current_games(room_id)

        # make a verification url for the friend game
        #verification_url = url_for("accept_friend_game", access_code=requested_room["accessCode"])
        return redirect(url_for("play", room_id=room_id))

    flash("This variant does not exist.")
    return redirect(url_for("index"))


@app.route("/rematch/<room_id>")
@login_required
@email_verified
def rematch(room_id: str):
    '''
    rematch a game
    :param room_id:
    :return:
    '''

    # get the room data from the room allocator
    room = room_manager.get_room(room_id)

    # blow out to index if the room doesn't exist
    if not room:
        flash("This room does not exist, cannot rematch.")
        return redirect(url_for('index'))

    # make sure the current user is in the room he's trying to rematch
    if current_user.id not in room["players"]:
        flash("You are not in this room so you cannot rematch this game.")
        return redirect(url_for("index"))

    # if the room is in progress, notify the player they cannot rematch until the game finishes
    if room["status"] != "finished":
        flash("You cannot rematch a game that is not finished yet.")
        return redirect(url_for("play", room_id=room_id))

    # actually try to rematch the game
    room["rematchReady"][current_user.id] = True
    room_manager.set_room_attribute(
          room_id=room_id
        , attribute="rematchReady"
        , value=room["rematchReady"]
    )
    # refresh the local room variable
    room = room_manager.get_room(room_id)

    # if all of the players are ready
    if all(v for k, v in room["rematchReady"]):
        # reset the room
        room_manager.reset_room(room_id)


    return redirect(url_for("play", room_id=room_id))


@app.route("/exit_game/<room_id>")
@login_required
@email_verified
def exit_game(room_id: str):
    '''
    update the player statistics of the game and clean it up
    :param room_id:
    :return:
    '''
    # update player statistics

    # clean up the game
    room_manager.clean_up_room(room_id)
    flash("thanks for playing!")
    return redirect(url_for("index"))


@app.route("/cancel_game/<room_id>")
@login_required
@email_verified
def cancel_game(room_id: str):
    '''
    just clean up the game and boot the player to the index
    :param room_id:
    :return:
    '''
    room_manager.clean_up_room(room_id)
    return redirect(url_for('index'))


