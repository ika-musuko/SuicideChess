from app import app, firebase
from flask import render_template

from .forms import FirePut

GETPOST = ['GET', 'POST']

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    fireform = FirePut()
    putdata = "previously entered data will appear here"
    print(firebase)
    if fireform.validate_on_submit():
        print("form submitted!")
        db = firebase.database()
        print(db)
        pushdata = {
             'name' : fireform.name.data
            ,'age' : fireform.age.data
            ,'graduated' : fireform.graduated.data
        }
        db.push(pushdata)
        flash("pushed data: %s" % pushdata)
        return redirect(url_for('index'))
        
    return render_template("index.html", form=fireform)
