from project import app

from flask import render_template

GETPOST = ['GET', 'POST']


### context processors ###
@app.context_processor
def inject_debug():
    return dict(debug=app.debug)

# decorators


### HOME PAGE ###
@app.route('/')
@app.route('/index')
def index() -> str:
    return render_template("index.html")


### ERROR HANDLING ###
@app.errorhandler(404)
def not_found_error(error):
    return "page not found 404 error: %s" % error, 404


@app.errorhandler(500)
def internal_error(error):
    return "internal server 500 error: %s" % error, 500


