from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired



"""
User login form
"""

class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired(message="The username is required")])
    password = PasswordField(u'Password', validators=[DataRequired(message="The password is required")])
    submit = SubmitField('Sign In')

class ExportDataForm(FlaskForm):

    inputs = SelectField('Inputs', choices=[('TIMES Signals', 'Signals'), ('TIMES Returns', 'Returns'), ('TIMES Positions','Positions')])
    submit_ok = SubmitField('Ok')

    start_date_inputs = StringField(u'Start Date', validators=[DataRequired(message="The username is required")])
    end_date_inputs = StringField(u'End Date', validators=[DataRequired(message="The username is required")])

    start_date_chart0 = StringField(u'Start Date')
    end_date_chart0 = StringField(u'End Date')

    start_date_chart1 = StringField(u'Start Date')
    end_date_chart1 = StringField(u'End Date')

    start_date_chart2 = StringField(u'Start Date')
    end_date_chart2 = StringField(u'End Date')

    start_date_chart3 = StringField(u'Start Date')
    end_date_chart3 = StringField(u'End Date')

    start_date_chart4 = StringField(u'Start Date')
    end_date_chart4 = StringField(u'End Date')

    start_date_chart5 = StringField(u'Start Date')
    end_date_chart5 = StringField(u'End Date')

    start_date_chart6 = StringField(u'Start Date')
    end_date_chart6 = StringField(u'End Date')

    submit_export = SubmitField('Export Data')
    submit_dates_chart = SubmitField('Ok')
    submit1 = SubmitField('ok')


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
    path_save_output_times = StringField(u'Path of the Outputs')
    name_file_times = StringField(u'Name of the File')
    submit_inputs = SubmitField('Submit Inputs to the Database')


