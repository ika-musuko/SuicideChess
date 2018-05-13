"""
error_views.py

    routes for error codes

    they should return a template string, in addition to the error code in a tuple

"""

from project import app
from flask import redirect, url_for, flash

@app.errorhandler(401)
def unauthorized_error(error):
    flash("401 - You are not authorized to view this page: %s" % (error))
    return redirect(url_for("index")), 401

@app.errorhandler(404)
def not_found_error(error):
    flash("404 - This page has not been found: %s" % (error))
    return redirect(url_for("index")), 404

@app.errorhandler(500)
def internal_error(error):
    return "internal server 500 error: %s" % error, 500
