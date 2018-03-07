from app import app, firebase
from flask import render_template, redirect, flash, url_for

from .forms import FirePut

GETPOST = ['GET', 'POST']

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    auth = firebase.auth()

    ID = "hi@nice.com"
    PW = "hinice"
    
    user = auth.sign_in_with_email_and_password(ID, PW)

    db = firebase.database()
    ddata = {
         'name' : 'flask'
        ,'age'  : 444344444
        ,'graduated' : False
    }
    #db.push(ddata, user['idToken'])

    fireform = FirePut()
    print("hi")
    if fireform.validate_on_submit():
        print("form submitted!")
        db = firebase.database()
        print(db)
        pushdata = {
             'name' : fireform.uname.data
            ,'age' : fireform.age.data
            ,'graduated' : fireform.graduated.data
        }
        db.push(pushdata, user['idToken'])
        flash("pushed data: %s" % pushdata)
        return redirect(url_for('index'))
        
    return render_template("index.html", form=fireform)
