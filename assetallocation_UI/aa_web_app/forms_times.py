from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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


class InputsTimesModel(FlaskForm):
    # Dates for dashboard
    start_date_times_inputs = StringField('Start Date')
    end_date_times_inputs = StringField('End Date')
    submit_ok_positions = SubmitField('ok')