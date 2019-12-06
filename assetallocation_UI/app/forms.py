from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

"""
User login form
"""
class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired(), Length(min=6, message='Passwords must be 6 charachters or greater.')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')





# class ChangePassword(FlaskForm):
#     old_password = PasswordField('Old Password', [DataRequired()])
#     new_password = PasswordField('New Password', [DataRequired(), EqualTo('confirm', message='Passwords must match'),Length(min=6, message='Passwords must be 6 charachters or greater.')])
#     confirm = PasswordField('Repeat Password')
#
# class AssetAllocationDetails(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Passwords must be 6 charachters or greater.')])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Sign In')