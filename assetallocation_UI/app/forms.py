from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

"""
User login form
"""
class LoginForm(FlaskForm):
    username = StringField(u'Username')
    password = PasswordField(u'Password')
    submit = SubmitField('Sign In')


