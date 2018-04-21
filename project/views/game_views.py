'''
game_views.py

    routes for the game

'''

from flask_login import login_required

from project import app
from project.views.view_utils import email_verified


@app.route('/play_blitz')
@login_required
@email_verified
def play_blitz() -> str:
    return 'blitz'


@app.route('/play_classic')
@login_required
@email_verified
def play_classic() -> str:
    return 'classic'