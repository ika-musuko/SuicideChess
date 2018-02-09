from flask import Flask
from firebase import firebase

app = Flask(__name__)
firebase = firebase.FirebaseApplication('https://flaskbase.firebaseio.com', 
None)

from app import routes, forms
