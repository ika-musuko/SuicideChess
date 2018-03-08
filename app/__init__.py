from flask import Flask
from flask_login import LoginManager
from config import Config
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)
app.config.from_object(Config)
lm = LoginManager(app)
#cred = credentials.Certificate("firebase_auth.json")
#firebase_app = firebase_admin.initialize_app(cred)

from app import routes
