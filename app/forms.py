from flask_wtf import Form
from wtforms import StringField, Booleanfield
from wtforms.validators import DataRequired
from app import firebase

class FirePut(Form):
    name = StringField('name', validators=[DataRequired()])

