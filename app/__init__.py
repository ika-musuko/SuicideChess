'''
__init__.py
initialization of the app
'''

# main flask imports
from flask import Flask
from flask_login import LoginManager

# firebase imports
from app import pyrebase_config, pyrebase_ext
from app.rooms import RoomManager
from app.new_game_data import NEW_GAME_DATA
import firebase_admin

# error logging imports
import logging
from logging.handlers import RotatingFileHandler # for error logging

# other general imports
import os

FIREBASE_APP_NAME = "flaskbase"

app = Flask(__name__)
app.config.from_pyfile("../config.py")
lm = LoginManager()
lm.init_app(app)


### FIREBASE ADMIN ###
# initialize the admin using initialize_firebase_admin.py
if FIREBASE_APP_NAME not in firebase_admin._apps:
    cred = firebase_admin.credentials.Certificate("firebase_auth.json")
    firebase_admin.initialize_app(cred, name=FIREBASE_APP_NAME)
fb_admin = firebase_admin.get_app(name=FIREBASE_APP_NAME)

### PYREBASE ###
pyre_firebase = pyrebase_ext.initialize_app(pyrebase_config.config) # see https://github.com/thisbejim/Pyrebase for details of pyrebase_config
pyre_auth = pyre_firebase.auth()
pyre_db = pyre_firebase.database()

### ROOM MANAGER ###
rm = RoomManager(db=pyre_db, game_branch="messagespam", new_game_data=NEW_GAME_DATA)

### ERROR LOGS ###
# make a rotating file handler to log errors to disk (future: email logging support?)
if not os.path.exists("logs"):
    os.mkdir("logs")
file_handler = RotatingFileHandler("logs/flaskbase.log", maxBytes=16384, backupCount=10)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler) # add it to the app's list of loggers

app.logger.setLevel(logging.INFO)
app.logger.info('flaskbase startup')

from app import routes, firebase_login, rooms
