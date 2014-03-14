from flask.ext.wtf import Form
from wtforms import validators, BooleanField, DateField, FloatField, StringField, IntegerField, DateTimeField


class LoginForm(Form):
    coreid = StringField(validators=[validators.Required()])
    password = StringField(validators=[validators.Required()])
    remember = BooleanField()
