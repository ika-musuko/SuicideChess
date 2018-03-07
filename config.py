import os

class Config():
    SECRET_KEY = os.environ.get("SECRET-KEY") or "twirtqow293tq20hgq"
    WTF_CSRF_ENABLED = True
    
