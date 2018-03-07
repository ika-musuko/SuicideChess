from flask import Flask
import pyrebase

app = Flask(__name__)
app.config.from_pyfile('../config.py')

PRJ_ID = "flaskbase"
API_KEY = "AIzaSyAe7PiL9pm_f4fAz1Nh5dg01jDb_TXEEYY"

firebase_config = {
     "apiKey" : API_KEY
    ,"authDomain" : PRJ_ID + ".firebaseapp.com"
    ,"databaseURL" : "https://" + PRJ_ID + ".firebaseio.com/"
    ,"storageBucket" : PRJ_ID + ".appspot.com"
    ,"messagingSenderId": "441451539007"
}

firebase = pyrebase.initialize_app(firebase_config)

from app import routes, forms
