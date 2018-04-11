from project import app

from flask import render_template

GETPOST = ['GET', 'POST']

### HOME PAGE ###
@app.route('/')
@app.route('/index')
def index() -> str:
    return render_template("index.html")

