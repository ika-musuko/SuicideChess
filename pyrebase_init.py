import os

import pyrebase_ext


def initialize_pyrebase():
    return pyrebase_ext.initialize_app({
          "apiKey" : os.getenv("PYREBASE_API_KEY") or ""
        , "authDomain" : os.getenv("PYREBASE_AUTH_DOMAIN") or ""
        , "databaseURL" : os.getenv("PYREBASE_DATABASE_URL") or ""
        , "storageBucket" : os.getenv("PYREBASE_STORAGE_BUCKET") or ""
        , "messagingSenderId" : os.getenv("PYREBASE_MESSAGING_SENDER_ID") or ""
    })