from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, FieldList, FormField
from wtforms.validators import DataRequired

from assetallocation_arp.common_libraries.dal_enums.strategy import Leverage, Frequency, DayOfWeek, Name
from assetallocation_UI.aa_web_app.service.strategy import get_strategy_versions
from assetallocation_UI.aa_web_app.service.fund import get_fund_names
from assetallocation_UI.aa_web_app.service.formatter import format_versions


class SideBarDataForm(FlaskForm):
    # Versions of the strategy
    existing_versions = get_strategy_versions(Name.times)
    version_choices = list(zip(existing_versions, format_versions(existing_versions)))

    # Chart Data
    versions_for_charts = SelectField('Versions', choices=version_choices)
    submit_ok_charts_data = SubmitField('ok')

    # Export data
    versions_for_export = SelectField('Versions', choices=version_choices)
    start_date_export = StringField()
    end_date_export = StringField()
    submit_ok_export_data = SubmitField('ok')


class AssetInputForm(FlaskForm):
    signal_ticker = StringField('signal_ticker')


class InputsTimesModel(FlaskForm):
    # Versions
    existing_versions = get_strategy_versions(Name.times)
    version_choices = [('New Version', 'New Version')]
    version_choices.extend(list(zip(existing_versions, format_versions(existing_versions))))
    versions = SelectField('Versions', choices=version_choices)
    submit_versions = SubmitField('Select this version')
    # submit_ok_charts_data = SubmitField('ok')
    # submit_ok_export_data = SubmitField('ok')

    # START_DATE = 'Start Date'
    # END_DATE = 'End Date'
    # start_date_times_inputs = StringField(START_DATE)
    # end_date_times_inputs = StringField(END_DATE)
    # submit_ok_positions = SubmitField('ok')

    # Fund names
    existing_funds = get_fund_names()
    input_fund_name_times = SelectField('Fund Name', choices=list(zip(existing_funds, existing_funds)))

    # Inputs
    strategy_weight = StringField(u'Strategy Weight', [DataRequired(message="The strategy weight is required")])
    time_lag = StringField(u'Time Lag', validators=[DataRequired(message="The time lag is required")])
    # leverage_type = SelectField('Leverage Type',
    #                             choices=[(Leverage.v.name, Leverage.v.name),
    #                                      (Leverage.n.name, Leverage.n.name),
    #                                      (Leverage.s.name, Leverage.s.name),
    #                                      (Leverage.e.name, Leverage.e.name)])
    volatility_window = StringField(u'Volatility Window', validators=[DataRequired(message="The volatility window is required")])
    sig1_short = StringField(u'Sigma1 short', validators=[DataRequired(message="The Sigma1 short is required")])
    sig1_long = StringField(u'Sigma1 long', validators=[DataRequired(message="The Sigma1 long is required")])
    sig2_short = StringField(u'Sigma2 short', validators=[DataRequired(message="The Sigma2 short is required")])
    sig2_long = StringField(u'Sigma2 long', validators=[DataRequired(message="The Sigma2 long is required")])
    sig3_short = StringField(u'Sigma3 short', validators=[DataRequired(message="The Sigma3 short is required")])
    sig3_long = StringField(u'Sigma3 long', validators=[DataRequired(message="The Sigma3 long is required")])

    # frequency = SelectField('Frequency',
    #                         choices=[(Frequency.weekly.name, Frequency.weekly.name),
    #                                  (Frequency.monthly.name, Frequency.monthly.name),
    #                                  (Frequency.daily.name, Frequency.daily.name),
    #                                  ])

    # week_day = SelectField('Week Day',
    #                        choices=[(DayOfWeek.MON.value, DayOfWeek.MON.name),
    #                                 (DayOfWeek.TUE.value, DayOfWeek.TUE.name),
    #                                 (DayOfWeek.WED.value, DayOfWeek.WED.name),
    #                                 (DayOfWeek.THU.value, DayOfWeek.THU.name),
    #                                 (DayOfWeek.FRI.value, DayOfWeek.FRI.name),
    #                                 (DayOfWeek.SAT.value, DayOfWeek.SAT.name),
    #                                 (DayOfWeek.SUN.value, DayOfWeek.SUN.name)]
    #                        )

    asset_input_set = FieldList(FormField(AssetInputForm), min_entries=0)

    # submit_save = SubmitField('Save')
