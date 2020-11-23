from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField


class InputsEffectStrategy(FlaskForm):
    version_choices = [('New Version', 'New Version')]  # TODO to automate
    versions_effect = SelectField('Versions', choices=version_choices)
    submit_ok_charts_effect_data = SubmitField('ok')

    start_date_effect_inputs = StringField('Start Date')
    end_date_effect_inputs = StringField('End Date')
    submit_ok_export_effect_data = SubmitField('ok')

    # Quarterly profit and loss
    start_date_quarterly_backtest_profit_and_loss_effect = StringField('31/03/2014')
    end_date_quarterly_backtest_profit_and_loss_effect = StringField('30/06/2017')
    start_date_quarterly_live_profit_and_loss_effect = StringField('30/09/2017')
    submit_ok_quarterly_profit_and_loss = SubmitField('ok')

    # Year to year contrib
    start_year_to_year_contrib = StringField('31/12/2019')
    submit_ok_year_to_year_contrib = SubmitField('ok')







