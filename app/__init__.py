from flask import Flask
from flask_login import LoginManager
from config import Config
import firebase_admin  # firebase admin SDK (for doing general firebase operations) 
import pyrebase # for using firebase as a user
from app import pyrebase_config
from firebase_admin import credentials

app = Flask(__name__)
app.config.from_object(Config)
lm = LoginManager(app)

# firebase admin
# initialize the admin using initialize_firebase_admin.py

cred = credentials.Certificate("firebase_auth.json")
firebase_admin.initialize_app(cred, name="flaskbase")
fb_admin = firebase_admin.get_app(name="flaskbase")

# pyrebase
pyre_firebase = pyrebase.initialize_app(pyrebase_config.config) # see https://github.com/thisbejim/Pyrebase for details of pyrebase_config
pyre_auth = pyre_firebase.auth()
pyre_db = pyre_firebase.database()

from app import routes
