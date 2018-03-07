from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from app import firebase

class FirePut(FlaskForm):
    uname = StringField('name', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    graduated = BooleanField('graduated')
    submit = SubmitField("add")
    

