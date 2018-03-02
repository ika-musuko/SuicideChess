# firebase/pyrebase sandbox
# adapted from https://kinformation.wjg.jp/blog/20170920-01
import pyrebase

# initialization
PRJ_ID = "flaskbase"
API_KEY = "AIzaSyBQ-BN1Tskv39oVKQOXb-vJI8CTKwge1gk"

config = {
     "apiKey" : API_KEY
    ,"authDomain" : PRJ_ID + ".firebaseapp.com"
    ,"databaseURL" : "https://" + PRJ_ID + ".firebaseio.com/"
    ,"storageBucket" : PRJ_ID + ".appspot.com"
    ,"messagingSenderId": "441451539007"

}

firebase = pyrebase.initialize_app(config)

# authentication
ID = "hi@nice.com"
PW = "hinice"

auth = firebase.auth()
user = auth.sign_in_with_email_and_password(ID, PW)

# database operations
db = firebase.database()
data = {"name" : "sherwyn", "age" : 21, "graduated" : False } # adding a single entry
db.push(data, user['idToken'])

"""
* push()
  automatically generated unique key is added
  
ex:
-----
flaskbase
  \_ -KuUQ8MRxcvTBt_GwyrN(unique)
    |_ "name": "sherwyn"
    |_ "age": 21
    \_ "graduated": false
"""

# updating a database entry
db.child("golgi").set(data, user['idToken'])

# getting a database entry
user_data = db.child("golgi").get(user['idToken'])
print(user_data.key())
print(user_data.val())