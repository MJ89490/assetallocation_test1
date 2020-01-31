from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

"""
User login form
"""
class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired(message="The username is required")])
    password = PasswordField(u'Password', validators=[DataRequired(message="The password is required")])
    submit = SubmitField('Sign In')


class ExportDataForm(FlaskForm):
    inputs = SelectField('Inputs', choices=[('TIMES Signals', 'Signals'), ('TIMES Returns', 'Returns'),('TIMES Positions','Positions')])
    submit_export = SubmitField('Export Data')
