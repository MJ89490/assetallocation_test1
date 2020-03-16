from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired
from assetallocation_arp.enum import leverage_types
from assetallocation_arp.enum import frequency_types

"""
User login form
"""


class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired(message="The username is required")])
    password = PasswordField(u'Password', validators=[DataRequired(message="The password is required")])
    submit = SubmitField('Sign In')


class ExportDataForm(FlaskForm):

    # todo link to the DB to grap the different versions automatically
    versions = SelectField('Versions', choices=[('Version1', 'Version1'), ('Version2', 'Version2'), ('Version3','Version3')])

    submit_ok_versions = SubmitField('Ok')

    leverage = SelectField('Leverage Types', choices=[(leverage_types.Leverage.v.name, leverage_types.Leverage.v.name ),
                                                      (leverage_types.Leverage.n.name, leverage_types.Leverage.n.name),
                                                      (leverage_types.Leverage.s.name, leverage_types.Leverage.s.name),
                                                      (leverage_types.Leverage.e.name, leverage_types.Leverage.e.name)])
    submit_ok_leverage = SubmitField('Ok')

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

    # todo link to the DB to grap the different versions automatically
    versions = SelectField('Versions',
                           choices=[('New Version', 'New Version'),('Version1', 'Version1'), ('Version2', 'Version2'), ('Version3', 'Version3')])
    submit_versions = SubmitField('Select this version')

    strategy_weight = StringField(u'Strategy Notional', [DataRequired(message="The strategy weight is required")])
    time_lag = StringField(u'Time Lag', validators=[DataRequired(message="The time lag is required")])
    leverage_type = SelectField('Leverage Type',
                                choices=[(leverage_types.Leverage.v.name, leverage_types.Leverage.v.name),
                                        (leverage_types.Leverage.n.name, leverage_types.Leverage.n.name),
                                        (leverage_types.Leverage.s.name, leverage_types.Leverage.s.name),
                                        (leverage_types.Leverage.e.name, leverage_types.Leverage.e.name)])
    volatility_window = StringField(u'Volatility Window', validators=[DataRequired(message="The volatility window is required")])
    sig1_short = StringField(u'Sigma1 short', validators=[DataRequired(message="The Sigma1 short is required")])
    sig1_long = StringField(u'Sigma1 long', validators=[DataRequired(message="The Sigma1 long is required")])
    sig2_short = StringField(u'Sigma2 short', validators=[DataRequired(message="The Sigma2 short is required")])
    sig2_long = StringField(u'Sigma2 long', validators=[DataRequired(message="The Sigma2 long is required")])
    sig3_short = StringField(u'Sigma3 short', validators=[DataRequired(message="The Sigma3 short is required")])
    sig3_long = StringField(u'Sigma3 long', validators=[DataRequired(message="The Sigma3 long is required")])

    frequency = SelectField('Frequency',
                            choices=[(frequency_types.Frequency.weekly.name, frequency_types.Frequency.weekly.name),
                                     (frequency_types.Frequency.monthly.name, frequency_types.Frequency.monthly.name),
                                     (frequency_types.Frequency.daily.name, frequency_types.Frequency.daily.name),
                                     ])

    week_day = SelectField('Week Day',
                           choices=[("MON", "MON"),
                                    ("TUE", "TUE"),
                                    ("WED", "WED"),
                                    ("THU", "THU"),
                                    ("FRI", "FRI"),
                                    ("SUN", "SUN"),
                                    ("SAT", "SAT")]
                           )

    name_file_times = StringField(u'Name of the File')
    save_excel_outputs = BooleanField('Save on Excel')
    save_db_outputs = BooleanField('Save in the DataBase')
    submit_save = SubmitField('Save')



