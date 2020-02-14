from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

"""
User login form
"""

DATES_CHOICES = [('Start Date', 'Start Date'),
                 ('30/05/2019', '30/05/2019'),
                 ('06/06/2019', '06/06/2019'),
                 ('13/06/2019', '13/06/2019'),
                 ('20/06/2019', '20/06/2019'),
                 ('27/06/2019', '27/06/2019')
                ]
DATES_END_CHOICES = [('End Date', 'End Date'),
                 ('30/05/2019', '30/05/2019'),
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
    inputs = SelectField('Inputs', choices=[('TIMES Signals', 'Signals'), ('TIMES Returns', 'Returns'), ('TIMES Positions','Positions')])
    start_date = SelectField('Start Date', choices=DATES_CHOICES)
    start_date_chart = SelectField('Start Date', choices=DATES_CHOICES)
    end_date = SelectField('End Date', choices=DATES_END_CHOICES)
    submit_ok = SubmitField('Ok')
    submit_export = SubmitField('Export Data')
    submit_dates_chart = SubmitField('Ok')


class InputsTimesModel(FlaskForm):
    strategy_weight = StringField(u'Strategy Weight', [DataRequired(message="The strategy weight is required")])
    time_lag = StringField(u'Time Lag', validators=[DataRequired(message="The time lag is required")])
    leverage_type = StringField(u'Leverage Type', validators=[DataRequired(message="The leverage type is required")])
    volatility_window = StringField(u'Volatility Window', validators=[DataRequired(message="The volatility window is required")])
    sig1_short = StringField(u'Sigma1 short', validators=[DataRequired(message="The Sigma1 short is required")])
    sig1_long = StringField(u'Sigma1 long', validators=[DataRequired(message="The Sigma1 long is required")])
    sig2_short = StringField(u'Sigma2 short', validators=[DataRequired(message="The Sigma2 short is required")])
    sig2_long = StringField(u'Sigma2 long', validators=[DataRequired(message="The Sigma2 long is required")])
    sig3_short = StringField(u'Sigma3 short', validators=[DataRequired(message="The Sigma3 short is required")])
    sig3_long = StringField(u'Sigma3 long', validators=[DataRequired(message="The Sigma3 long is required")])
    frequency = StringField(u'Frequency', validators=[DataRequired(message="The frequency is required")])
    week_day = StringField(u'Week Day', validators=[DataRequired(message="The week day is required")])
    submit_inputs = SubmitField('Submit Inputs to the Database')
    submit_run_times_model = SubmitField('Run the model')

