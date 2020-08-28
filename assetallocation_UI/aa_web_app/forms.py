from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired

from assetallocation_arp.common_libraries.dal_enums.strategy import Leverage, Frequency, DayOfWeek, Name
from assetallocation_UI.aa_web_app.service.strategy import get_strategy_versions
from assetallocation_UI.aa_web_app.service.fund import get_fund_names
from assetallocation_UI.aa_web_app.service.formatter import format_versions

"""
User login form
"""


class LoginForm(FlaskForm):
    username = StringField(u'Username')
    password = PasswordField(u'Password')
    submit = SubmitField('Sign In')


class ExportDataForm(FlaskForm):

    START_DATE = 'Start Date'
    END_DATE = 'End Date'

    existing_versions = get_strategy_versions(Name.times)
    versions = SelectField('Versions', choices=list(zip(existing_versions, format_versions(existing_versions))))

    submit_ok_versions = SubmitField('Ok')

    leverage = SelectField('Leverage Types', choices=[(Leverage.v.name, Leverage.v.name ),
                                                      (Leverage.n.name, Leverage.n.name),
                                                      (Leverage.s.name, Leverage.s.name),
                                                      (Leverage.e.name, Leverage.e.name)])
    submit_ok_leverage = SubmitField('Ok')

    inputs = SelectField('Inputs', choices=[('TIMES Signals', 'Signals'), ('TIMES Returns', 'Returns'), ('TIMES Positions','Positions')])
    submit_ok = SubmitField('Ok')

    # todo create a common button class and gives the inputs

    start_date_inputs = StringField(START_DATE)
    end_date_inputs = StringField(END_DATE)

    start_date_chart0 = StringField(START_DATE)
    end_date_chart0 = StringField(END_DATE)

    start_date_chart1 = StringField(START_DATE)
    end_date_chart1 = StringField(END_DATE)

    start_date_chart2 = StringField(START_DATE)
    end_date_chart2 = StringField(END_DATE)

    start_date_chart3 = StringField(START_DATE)
    end_date_chart3 = StringField(END_DATE)

    start_date_chart4 = StringField(START_DATE)
    end_date_chart4 = StringField(END_DATE)

    start_date_chart5 = StringField(START_DATE)
    end_date_chart5 = StringField(END_DATE)

    start_date_chart6 = StringField(START_DATE)
    end_date_chart6 = StringField(END_DATE)

    submit_export = SubmitField(START_DATE)
    submit_dates_chart = SubmitField('Ok')
    submit1 = SubmitField('ok')


class InputsTimesModel(FlaskForm):
    existing_versions = get_strategy_versions(Name.times)
    version_choices = [('New Version', 'New Version')]
    version_choices.extend(list(zip(existing_versions, format_versions(existing_versions))))
    versions = SelectField('Versions', choices=version_choices)

    submit_versions = SubmitField('Select this version')

    existing_funds = get_fund_names()
    fund_name = SelectField('Fund Name', choices=list(zip(existing_funds, existing_funds)))

    strategy_weight = StringField(u'Strategy Weight', [DataRequired(message="The strategy weight is required")])
    time_lag = StringField(u'Time Lag', validators=[DataRequired(message="The time lag is required")])
    leverage_type = SelectField('Leverage Type',
                                choices=[(Leverage.v.name, Leverage.v.name),
                                         (Leverage.n.name, Leverage.n.name),
                                         (Leverage.s.name, Leverage.s.name),
                                         (Leverage.e.name, Leverage.e.name)])
    volatility_window = StringField(u'Volatility Window', validators=[DataRequired(message="The volatility window is required")])
    sig1_short = StringField(u'Sigma1 short', validators=[DataRequired(message="The Sigma1 short is required")])
    sig1_long = StringField(u'Sigma1 long', validators=[DataRequired(message="The Sigma1 long is required")])
    sig2_short = StringField(u'Sigma2 short', validators=[DataRequired(message="The Sigma2 short is required")])
    sig2_long = StringField(u'Sigma2 long', validators=[DataRequired(message="The Sigma2 long is required")])
    sig3_short = StringField(u'Sigma3 short', validators=[DataRequired(message="The Sigma3 short is required")])
    sig3_long = StringField(u'Sigma3 long', validators=[DataRequired(message="The Sigma3 long is required")])

    frequency = SelectField('Frequency',
                            choices=[(Frequency.weekly.name, Frequency.weekly.name),
                                     (Frequency.monthly.name, Frequency.monthly.name),
                                     (Frequency.daily.name, Frequency.daily.name),
                                     ])

    week_day = SelectField('Week Day',
                           choices=[(DayOfWeek.MON.value, DayOfWeek.MON.name),
                                    (DayOfWeek.TUE.value, DayOfWeek.TUE.name),
                                    (DayOfWeek.WED.value, DayOfWeek.WED.name),
                                    (DayOfWeek.THU.value, DayOfWeek.THU.name),
                                    (DayOfWeek.FRI.value, DayOfWeek.FRI.name),
                                    (DayOfWeek.SAT.value, DayOfWeek.SAT.name),
                                    (DayOfWeek.SUN.value, DayOfWeek.SUN.name)]
                           )

    submit_save = SubmitField('Save')



