from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired

from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_UI.aa_web_app.service.strategy import get_strategy_versions
from assetallocation_UI.aa_web_app.service.fund import get_fund_names
from assetallocation_UI.aa_web_app.service.formatter import format_versions


class SideBarDataForm(FlaskForm):
    # Versions of the strategy
    existing_versions = get_strategy_versions(Name.times)
    versions = []

    input_versions_times = format_versions(existing_versions)

    # Fund name
    existing_funds = get_fund_names()
    input_fund_name_times = existing_funds


# class AssetInputForm(FlaskForm):
#     signal_ticker = StringField('signal_ticker')


class InputsTimesModel(FlaskForm):
    # # Versions TO REMOVE later
    # existing_versions = get_strategy_versions(Name.times)

    # input_versions_times = format_versions(existing_versions)

    # Fund names
    # existing_funds = get_fund_names()
    # input_fund_name_times = SelectField('Fund Name', choices=list(zip(existing_funds, existing_funds)))

    # Dates for dashboard
    start_date_times_inputs = StringField('Start Date')
    end_date_times_inputs = StringField('End Date')
    submit_ok_positions = SubmitField('ok')

    # Inputs
    strategy_weight = StringField(u'Strategy Weight', [DataRequired(message="The strategy weight is required")])
    time_lag = StringField(u'Time Lag', validators=[DataRequired(message="The time lag is required")])

    volatility_window = StringField(u'Volatility Window', validators=[DataRequired(message="The volatility window is required")])
    sig1_short = StringField(u'Sigma1 short', validators=[DataRequired(message="The Sigma1 short is required")])
    sig1_long = StringField(u'Sigma1 long', validators=[DataRequired(message="The Sigma1 long is required")])
    sig2_short = StringField(u'Sigma2 short', validators=[DataRequired(message="The Sigma2 short is required")])
    sig2_long = StringField(u'Sigma2 long', validators=[DataRequired(message="The Sigma2 long is required")])
    sig3_short = StringField(u'Sigma3 short', validators=[DataRequired(message="The Sigma3 short is required")])
    sig3_long = StringField(u'Sigma3 long', validators=[DataRequired(message="The Sigma3 long is required")])

    # asset_input_set = FieldList(FormField(AssetInputForm), min_entries=0)
