'''
config.py
configuration file for flask
'''

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY") or "twirtqow293tq20hgq"

### WTForms config ###
WTF_CSRF_ENABLED = True


