from flask_login import login_required

from project import app
from project.views.view_decorators import email_verified


@app.route('/play_random')
@login_required
@email_verified
def play_random() -> str:
    return 'play random'


@app.route('/play_friend')
@login_required
@email_verified
def play_friend() -> str:
    return 'play friend'