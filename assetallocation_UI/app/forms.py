from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

"""
User login form
"""
class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired(message="The username is required")])
    password = PasswordField(u'Password', validators=[DataRequired(message="The password is required")])
    submit = SubmitField('Sign In')


