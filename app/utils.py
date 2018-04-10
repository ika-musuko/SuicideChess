import requests
import json

def get_firebase_error_message(e: requests.exceptions.HTTPError):
    return json.loads(e.args[1])["error"]["message"]