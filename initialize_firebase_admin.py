import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate("firebase_auth.json")
fb_admin = firebase_admin.initialize_app(cred, name="flaskbase")
print(fb_admin)
