from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

"""
User login form
"""

DATES_CHOICES = [('30/05/2019', '30/05/2019'),
                 ('06/06/2019', '06/06/2019'),
                 ('13/06/2019', '13/06/2019'),
                 ('20/06/2019', '20/06/2019'),
                 ('27/06/2019', '27/06/2019')
                ]

class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired(message="The username is required")])
    password = PasswordField(u'Password', validators=[DataRequired(message="The password is required")])
    submit = SubmitField('Sign In')


class ExportDataForm(FlaskForm):
    inputs = SelectField('Inputs', choices=[('TIMES Signals', 'Signals'), ('TIMES Returns', 'Returns'),('TIMES Positions','Positions')])
    start_date = SelectField('Start Date', choices=DATES_CHOICES)
    end_date = SelectField('End Date', choices=DATES_CHOICES)
    submit_ok = SubmitField('Ok')
    submit_export = SubmitField('Export Data')
