'''
error_views.py

    routes for error codes

    they should return a template string, in addition to the error code in a tuple

'''

from project import app


@app.errorhandler(404)
def not_found_error(error):
    return "page not found 404 error: %s" % error, 404


@app.errorhandler(500)
def internal_error(error):
    return "internal server 500 error: %s" % error, 500