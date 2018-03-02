from flask import Flask
import pyrebase
import firebase_config

app = Flask(__name__)
app.config.from_pyfile('../config.py')

firebase = pyrebase.initialize_app(firebase_config.firebase_config)

from app import routes, forms
