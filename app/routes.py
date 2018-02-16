from app import app, firebase
from flask import render_template

from .forms import FirePut

GETPOST = ['GET', 'POST']

@app.route('/', methods=GETPOST)
@app.route('/index', methods=GETPOST)
def index():
    fireform = FirePut()
    putdata = "previously entered data will appaer here"
    if fireform.validate_on_submit():
        putdata = {'Name' : fireform.name.data}
        firebase.put('/names', name)
    return render_template("index.html", form=fireform, putdata=putdata)
