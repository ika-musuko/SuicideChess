from flask import Flask
from firebase import firebase as fb

app = Flask(__name__)
app.config.from_pyfile('../config.py')
firebase = fb.FirebaseApplication('https://flaskbase.firebaseio.com', None)

from app import routes, forms
