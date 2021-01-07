import json

from flask import render_template
from flask import request, redirect, url_for

from assetallocation_UI.aa_web_app import app
from assetallocation_UI.aa_web_app.forms_times import InputsTimesModel, SideBarDataForm
from assetallocation_UI.aa_web_app.forms_effect import InputsEffectStrategy
from assetallocation_UI.aa_web_app.data_import.compute_charts_data import TimesChartsDataComputations
from assetallocation_UI.aa_web_app.data_import.main_import_data import run_times_charts_data_computations

from aa_web_app.data_import.get_data_times import ReceivedDataTimes
from aa_web_app.data_import.get_data_effect import ProcessDataEffect
from aa_web_app.data_import.download_data_chart_effect import DownloadDataChartEffect

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
    show_versions, show_versions_export = 'show_versions_not_available', 'show_versions_not_available'  # TODO move at the top
    positions_chart, do_not_run = False, False

    if request.method == 'POST':
        if form.submit_ok_positions.data:
            positions_chart = True
            start, end = request.form['start_date_box_times'], request.form['end_date_box_times']
            positions, dates_pos, names_pos = obj_times_charts_data.compute_positions_assets(start_date=start,
                                                                                             end_date=end)
        elif request.form['submit_button'] == 'dashboard':
            obj_received_data_times.receive_data_latest_version_dashboard()

        obj_times_charts_data.call_times_proc_caller(obj_received_data_times.fund_name,
                                                     obj_received_data_times.version_strategy)
        template_data = run_times_charts_data_computations(obj_times_charts_data,
                                                           obj_received_data_times.strategy_weight,
                                                           start_date_sum=None, start_date=None, end_date=None)
        if positions_chart:
            template_data['positions'], template_data['dates_pos'], template_data['names_pos'] = positions, dates_pos, names_pos

    else:
        if obj_received_data_times.type_of_request == 'export_data_sidebar':
            obj_times_charts_data.call_times_proc_caller(obj_received_data_times.fund_name,
                                                         obj_received_data_times.version_strategy)
            obj_times_charts_data.export_times_data_to_csv()
        else:
            obj_received_data_times.receive_data_selected_version_sidebar_dashboard()
            obj_times_charts_data.call_times_proc_caller(obj_received_data_times.fund_name,
                                                         obj_received_data_times.version_strategy)
            template_data = run_times_charts_data_computations(obj_times_charts_data,
                                                               obj_received_data_times.strategy_weight,
                                                               start_date_sum=None, start_date=None, end_date=None)

    return render_template('times_dashboard.html',
                           title='Dashboard',
                           form=form,
                           show_versions=show_versions,
                           show_versions_export=show_versions_export,
                           form_side_bar=form_side_bar,
                           fund_strategy=obj_received_data_times.fund_strategy_dict,
                           fund_list=form_side_bar.input_fund_name_times,
                           versions_list=form_side_bar.input_versions_times,
                           **template_data)


@app.route('/times_strategy', methods=['GET', 'POST'])
def times_strategy():
    form = InputsTimesModel()
    show_versions = 'show_versions_not_available'
    show_dashboard = 'show_dashboard_not_available'
    run_model_page = 'not_run_model'
    assets = []

    if request.method == 'POST':
        if request.form['submit_button'] == 'select-fund':
            obj_received_data_times.fund_name = form.input_fund_name_times.data
            show_versions = 'show_versions_available'
            show_dashboard = 'show_dashboard'
        elif request.form['submit_button'] == 'select-versions':
            version_strategy = form.versions.data
            if version_strategy == 'New Version':
                run_model_page = 'run_new_version'
            else:
                run_model_page = 'run_existing_version'
                assets = obj_received_data_times.receive_data_existing_versions(strategy_version=version_strategy)

        elif request.form['submit_button'] == 'run-strategy-existing-versions':
            obj_received_data_times.run_existing_strategy()

            return redirect(url_for('times_dashboard'))

    return render_template('times_template.html',
                           title='TimesPage',
                           form=form,
                           show_versions=show_versions,
                           run_model_page=run_model_page,
                           show_dashboard=show_dashboard,
                           assets=assets,
                           inputs_versions=obj_received_data_times.inputs_existing_versions_times)


@app.route('/received_data_times_form', methods=['POST'])
def received_data_times_form():
    form_data = request.form['form_data'].split('&')
    obj_received_data_times.is_new_strategy = True
    obj_received_data_times.received_data_times(form_data)
    obj_received_data_times.call_run_times(json.loads(request.form['json_data']))
    return json.dumps({'status': 'OK'})


@app.route('/receive_sidebar_data_times_form', methods=['POST'])
def receive_sidebar_data_times_form():
    outputs_sidebar = json.loads(request.form['json_data'])
    obj_received_data_times.version_strategy = outputs_sidebar['inputs_version']
    obj_received_data_times.fund_name = outputs_sidebar['input_fund']
    obj_received_data_times.type_of_request = outputs_sidebar['type_of_request']

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
    obj_received_data_times.is_new_strategy = True
    effect_form = obj_received_data_effect.receive_data_effect(form_data)
    obj_received_data_effect.call_run_effect(assets_inputs_effect=json.loads(request.form['json_data']))
    return json.dumps({'status': 'OK', 'effect_data': effect_form})


@app.route('/risk_returns', methods=['GET', 'POST'])
def risk_returns():
    effect_outputs = obj_received_data_effect.effect_outputs
    return render_template('risk_returns_template.html',
                           title='Risk_Returns_overall',
                           effect_outputs=effect_outputs)
