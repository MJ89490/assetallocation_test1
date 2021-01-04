import json

from flask import render_template
from flask import request

from assetallocation_UI.aa_web_app import app
from assetallocation_UI.aa_web_app.forms_times import InputsTimesModel, SideBarDataForm
from assetallocation_UI.aa_web_app.forms_effect import InputsEffectStrategy

from aa_web_app.data_import.get_data_times import ReceivedDataTimes
from aa_web_app.data_import.get_data_effect import ProcessDataEffect

from aa_web_app.data_import.download_data_chart_effect import DownloadDataChartEffect

from assetallocation_UI.aa_web_app.data_import.compute_charts_data import TimesChartsDataComputations
from assetallocation_UI.aa_web_app.data_import.main_import_data import run_times_charts_data_computations

from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller
from assetallocation_arp.common_libraries.dal_enums.strategy import Name

obj_received_data_effect = ProcessDataEffect()
obj_received_data_times = ReceivedDataTimes()
obj_download_data_effect = DownloadDataChartEffect()

obj_times_charts_data = TimesChartsDataComputations()


@app.route('/')
def home():
    return render_template('home.html', title='HomePage')


@app.route('/times_dashboard',  methods=['GET', 'POST'])
def times_dashboard():
    form = InputsTimesModel()
    form_side_bar = SideBarDataForm()

    positions_chart = False

    if request.method == 'POST':
        if form.submit_ok_positions.data:
            positions_chart = True
            start, end = request.form['start_date_box_times'], request.form['end_date_box_times']
            positions, dates_pos, names_pos = obj_times_charts_data.compute_positions_assets(start_date=start, end_date=end)
        elif request.form['submit_button'] == 'dashboard':
            apc = TimesProcCaller()
            f, obj_received_data_times.fund_name = 'f1', 'f1'
            strategy, obj_received_data_times.version_strategy = max(apc.select_strategy_versions(Name.times)), \
                                                                 max(apc.select_strategy_versions(Name.times))
            fs = apc.select_fund_strategy_results(f, Name.times, strategy)
            obj_received_data_times.strategy_weight = fs.weight

    obj_times_charts_data.call_times_proc_caller(obj_received_data_times.fund_name, obj_received_data_times.version_strategy)
    template_data = run_times_charts_data_computations(obj_times_charts_data,
                                                       obj_received_data_times.strategy_weight,
                                                       start_date_sum=None, start_date=None, end_date=None)
    if positions_chart:
        template_data['positions'], template_data['dates_pos'], template_data['names_pos'] = positions, \
                                                                                             dates_pos, \
                                                                                             names_pos

    return render_template('times_dashboard.html',
                           title='Dashboard',
                           form=form,
                           form_side_bar=form_side_bar,
                           fund_strategy=obj_received_data_times.fund_strategy_dict,
                           **template_data)


@app.route('/times_strategy', methods=['GET', 'POST'])
def times_strategy():
    form = InputsTimesModel()
    show_versions = 'show_versions_not_available'
    run_model_page = 'not_run_model_page'

    if request.method == 'POST':
        if request.form['submit_button'] == 'select-fund':
            obj_received_data_times.fund_name =  form.input_fund_name_times.data
            show_versions = 'show_versions_available'
        elif request.form['submit_button'] == 'select-versions':
            run_model_page = 'run_model_page'

    return render_template('times_template.html',
                           title='TimesPage',
                           form=form,
                           show_versions=show_versions,
                           run_model_page=run_model_page)


@app.route('/received_data_times_form', methods=['POST'])
def received_data_times_form():
    form_data = request.form['form_data'].split('&')
    obj_received_data_times.received_data_times(form_data)
    obj_received_data_times.call_run_times(json.loads(request.form['json_data']))
    return json.dumps({'status': 'OK'})


@app.route('/effect_dashboard',  methods=['GET', 'POST'])
def effect_dashboard():
    form = InputsEffectStrategy()

    if request.method == "POST":
        if form.submit_ok_quarterly_profit_and_loss.data:
            obj_received_data_effect.start_quarterly_back_p_and_l_date = form.start_date_quarterly_backtest_profit_and_loss_effect.data
            obj_received_data_effect.end_quarterly_back_p_and_l_date = form.end_date_quarterly_backtest_profit_and_loss_effect.data
            obj_received_data_effect.start_quarterly_live_p_and_l_date = form.start_date_quarterly_live_profit_and_loss_effect.data
        elif form.submit_ok_year_to_year_contrib.data:
            obj_received_data_effect.start_year_to_year_contrib_date = form.start_year_to_year_contrib.data

        elif request.form['submit_button'] == 'year_to_year_contrib_download':
            obj_received_data_effect.download_year_to_year_contrib_chart()
        elif request.form['submit_button'] == 'region_download':
            obj_received_data_effect.download_regions_charts()
        elif request.form['submit_button'] == 'agg_download':
            obj_received_data_effect.download_aggregate_chart()
        elif request.form['submit_button'] == 'drawdown_download':
            obj_received_data_effect.download_drawdown_chart()
        elif request.form['submit_button'] == 'quarterly_download':
            obj_received_data_effect.download_quarterly_profit_and_loss_chart()

    data_effect = obj_received_data_effect.run_process_data_effect()

    return render_template('effect_dashboard.html',
                           form=form,
                           data_effect=data_effect,
                           title='Dashboard')


@app.route('/effect_strategy', methods=['GET', 'POST'])
def effect_strategy():
    form = InputsEffectStrategy()
    if request.method == 'GET':
        run_model_page = 'not_run_model_page'
    else:
        run_model_page = 'run_model_page'
    return render_template('effect_template.html',
                           title='EffectPage',
                           form=form,
                           run_model_page=run_model_page)


@app.route('/received_data_effect_form', methods=['POST'])
def received_data_effect_form():
    form_data = request.form['form_data'].split('&')
    effect_form = obj_received_data_effect.receive_data_effect(form_data)
    obj_received_data_effect.call_run_effect(assets_inputs_effect=json.loads(request.form['json_data']))
    return json.dumps({'status': 'OK', 'effect_data': effect_form})


@app.route('/risk_returns', methods=['GET', 'POST'])
def risk_returns():
    effect_outputs = obj_received_data_effect.effect_outputs
    return render_template('risk_returns_template.html',
                           title='Risk_Returns_overall',
                           effect_outputs=effect_outputs)
