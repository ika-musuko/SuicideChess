import urllib2
from flask import Flask
import unittest
import flask_testing

from project import app

class WebAppTestCase(flask_testing.TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

if __name__ == "__main__":
    unittest.main()