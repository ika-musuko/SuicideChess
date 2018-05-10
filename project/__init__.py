'''
__init__.py
initialization of the project
'''
# project imports

# main flask imports
from flask import Flask
from flask_login import LoginManager


# firebase imports
import pyrebase_ext

# google login imports
from flask_dance.contrib.google import make_google_blueprint

# models imports
from project.rooms.room_manager import RoomManager
from project.models.new_game_data import NEW_GAME_DATA
from project.players.player_manager import PlayerManager

# error logging imports
import logging
from logging.handlers import RotatingFileHandler # for error logging

# other general imports
import os

FIREBASE_APP_NAME = os.getenv("FIREBASE_APP_NAME") or "flaskbase"

app = Flask(__name__)
app.config.from_pyfile("../config/config.py")

# flask login
lm = LoginManager()
lm.init_app(app)


### FIREBASE ADMIN ###
# initialize the admin using initialize_firebase_admin.py
'''
if FIREBASE_APP_NAME not in firebase_admin._apps:
    cred = firebase_admin.credentials.Certificate("config/firebase_auth.json")
    firebase_admin.initialize_app(cred, name=FIREBASE_APP_NAME)
fb_admin = firebase_admin.get_app(name=FIREBASE_APP_NAME)
'''

### PYREBASE ###
pyre_firebase = pyrebase_ext.initialize_app({
      "apiKey" : os.getenv("PYREBASE_API_KEY") or ""
    , "authDomain" : os.getenv("PYREBASE_AUTH_DOMAIN") or ""
    , "databaseURL" : os.getenv("PYREBASE_DATABASE_URL") or ""
    , "storageBucket" : os.getenv("PYREBASE_STORAGE_BUCKET") or ""
    , "messagingSenderId" : os.getenv("PYREBASE_MESSAGING_SENDER_ID") or ""
})
pyre_db = pyre_firebase.database()

### GOOGLE LOGIN ###
GOOGLE_AUTH_KEYS = {
      "GOOGLE_CLIENT_ID" : os.getenv("GOOGLE_CLIENT_ID") or ""
    , "GOOGLE_CLIENT_SECRET" : os.getenv("GOOGLE_CLIENT_SECRET") or ""
}

### ROOM MANAGER ###
room_manager = RoomManager(db=pyre_db, game_branch="SuicideChess", new_game_data=NEW_GAME_DATA)

### PLAYER MANAGER ###
player_manager = PlayerManager(db=pyre_db, user_branch="users")

### ERROR LOGS ###
# make a rotating file handler to log errors to disk (future: email logging support?)
if not os.path.exists("logs"):
    os.mkdir("logs")
file_handler = RotatingFileHandler("logs/flaskbase.log", maxBytes=16384, backupCount=10)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler) # add it to the project's list of loggers

app.logger.setLevel(logging.INFO)
app.logger.info('flaskbase startup')

from project.views import auth_views, game_views, home_views
from project.auth import firebase_login
