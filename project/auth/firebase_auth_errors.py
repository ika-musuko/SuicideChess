'''
firebase_auth_errors.py

functions for handling firebase authentication error responses
'''

import json, requests

ERROR_MAP = {
      "EMAIL_EXISTS" : "This email already exists. Please log in with your credentials."
    , "OPERATION_NOT_ALLOWED" : "Password sign-in is not allowed"
    , "TOO_MANY_ATTEMPTS_TRY_LATER" : "This account has received too much unusual activity. Please try again later."
    , "TOKEN_EXPIRED" : "This credential is no longer valid. Please sign in again."
    , "USER_NOT_FOUND" : "This user has not been found."
    , "USER_DISABLED" : "This account has been disabled by an administrator."
    , "EMAIL_NOT_FOUND" : "There is no user record corresponding to this identifier. The user may have been deleted."
    , "INVALID_PASSWORD" : "Your password is incorrect."
    , "WEAK_PASSWORD" : "Your password must be more than six characters."
    , "INVALID_EMAIL" : "This email address is invalid."
}


def error_map(response: str):
    '''
    get a real error message from a firebase error response
    :param response: firebase error response
    :return: the associated error message
    '''
    return ERROR_MAP[response] if response in ERROR_MAP else response


def get_firebase_error_message(e: requests.exceptions.HTTPError):
    '''
    get the firebase error response
    :param e: the firebase HTTPError
    :return: the error response
    '''
    return json.loads(e.args[1])["error"]["message"]