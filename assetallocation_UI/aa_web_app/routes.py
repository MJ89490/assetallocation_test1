import os
import json
from flask import render_template
from flask import request, redirect, url_for, jsonify, make_response

from assetallocation_UI.aa_web_app import app

from assetallocation_UI.aa_web_app.service.fund import get_fund_names
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_UI.aa_web_app.forms_effect import InputsEffectStrategy
from assetallocation_UI.aa_web_app.service.formatter import format_versions
from assetallocation_UI.aa_web_app.service.strategy import get_strategy_versions
from assetallocation_UI.aa_web_app.data_import.get_data_effect import ProcessDataEffect
from assetallocation_UI.aa_web_app.forms_times import InputsTimesModel, SideBarDataForm
from assetallocation_UI.aa_web_app.data_import.receive_data_times import ReceiveDataTimes
from assetallocation_UI.aa_web_app.data_import.compute_data_dashboard_times import ComputeDataDashboardTimes
from assetallocation_UI.aa_web_app.data_import.main_compute_data_dashboard_times import main_compute_data_dashboard_times
from assetallocation_UI.aa_web_app.data_import.call_times_proc_caller import call_times_proc_caller, \
    call_times_select_all_fund_strategy_result_dates
from assetallocation_UI.aa_web_app.data_import.download_data_strategy_to_domino import export_times_data_to_csv, \
    export_times_positions_data_to_csv


obj_received_data_times = ReceiveDataTimes()
obj_received_data_effect = ProcessDataEffect()


@app.route('/',  methods=['GET'])
def home():
    r = make_response(render_template('home.html', title='HomePage'))
    if os.sys.platform == 'win32':
        r.set_cookie(key='username', value=os.environ.get('USERNAME'), max_age=None)
    return r


# @app.route('/')
# def home():
#     return render_template('home.html', title='HomePage')


@app.route('/times_strategy', methods=['GET', 'POST'])
def times_strategy():
    global obj_received_data_times
    run_model_page = 'not_run_model'
    assets, asset_tickers_names_subcategories = [], []
    fund_selected, pop_up_message = '', ''
    existing_versions_from_db = format_versions(get_strategy_versions(Name.times))
    existing_funds_from_db = get_fund_names()

    if request.method == 'POST':
        if request.form['submit_button'] == 'new-version':
            run_model_page = 'run_new_version'
            asset_tickers_names_subcategories = obj_received_data_times.select_tickers()
        else:
            obj_received_data_times.receive_data_existing_versions(strategy_version=
                                                                   obj_received_data_times.version_strategy)
            obj_received_data_times.run_existing_strategy()
            return redirect(url_for('times_charts_dashboard'))
    else:

        if obj_received_data_times.match_date_db is False:
            assets = obj_received_data_times.receive_data_existing_versions(strategy_version=
                                                                            obj_received_data_times.version_strategy)
            run_model_page = 'run_existing_version'
            # Reset the match date
            obj_received_data_times.match_date_db = None

        if obj_received_data_times.match_date_db:
            pop_up_message = 'pop_up_message'
            assets = obj_received_data_times.receive_data_existing_versions(strategy_version=
                                                                            obj_received_data_times.version_strategy)
            # Reset the match date
            obj_received_data_times.match_date_db = None

    return render_template('times_template.html',
                           title='TimesPage',
                           fund_selected=obj_received_data_times.fund_name,
                           asset_tickers_names_subcategories=asset_tickers_names_subcategories,
                           version_selected=obj_received_data_times.version_strategy,
                           existing_funds_from_db=existing_funds_from_db,
                           pop_up_message=pop_up_message,
                           run_model_page=run_model_page,
                           assets=assets,
                           existing_versions_from_db=existing_versions_from_db,
                           inputs_versions=obj_received_data_times.inputs_existing_versions_times)


@app.route('/receive_data_from_times_strategy_page', methods=['POST'])
def receive_data_from_times_strategy_page():
    #global obj_received_data_times
    json_data = json.loads(request.form['json_data'])
    try:
        obj_received_data_times.type_of_request = json_data['run_existing-version']
    except KeyError:
        pass
    print(f"receive_data_from_times_strategy_page = {json_data}", flush=True)
    if json_data['type_of_request'] == 'selected_fund':
        print(json_data['fund'])
        obj_received_data_times.fund_name = json_data['fund']
    elif json_data['type_of_request'] == 'selected_fund_weight':
        obj_received_data_times.strategy_weight_user = json_data['strategy_weight']
    elif json_data['type_of_request'] == 'selected_version_date_to':
        obj_received_data_times.version_strategy = json_data['version']
        obj_received_data_times.date_to = json_data['date_to']
        obj_received_data_times.match_date_db = obj_received_data_times.check_in_date_to_existing_version()
    elif json_data['type_of_request'] == 'selected_ticker':
        obj_received_data_times.type_of_request = json_data['type_of_request']
        name, subcategory = obj_received_data_times.select_names_subcategories(json_data['input_signal_ticker_from_times'])
        return jsonify({'name': name, 'subcategory': subcategory})

    return json.dumps({'status': 'OK'})


@app.route('/receive_data_from_times_strategy_form', methods=['POST'])
def receive_data_from_times_strategy_form():
    global obj_received_data_times
    form_data = request.form['form_data'].split('&')
    json_data = json.loads(request.form['json_data'])
    form_data.append('input_version_name=' + json_data['input_version_name_strategy'])
    obj_received_data_times.version_description = json_data["input_version_name_strategy"]
    obj_received_data_times.is_new_strategy = True
    obj_received_data_times.received_data_times(form_data)
    obj_received_data_times.call_run_times(json_data)

    return json.dumps({'status': 'OK'})


@app.route('/receive_sidebar_data_times_form', methods=['POST'])
def receive_sidebar_data_times_form():
    global obj_received_data_times
    outputs_sidebar = json.loads(request.form['json_data'])

    if outputs_sidebar['type_of_request'] == 'date_to_data_sidebar':
        obj_received_data_times.date_to_sidebar = outputs_sidebar['inputs_date_to']

    elif outputs_sidebar['type_of_request'] == 'date_to_export_data_sidebar':
        obj_received_data_times.date_to_export_sidebar = outputs_sidebar['inputs_date_to']

    elif outputs_sidebar['type_of_request'] == 'export_data_sidebar':
        obj_received_data_times.version_strategy_export = outputs_sidebar['inputs_version']
        obj_received_data_times.fund_name_export = outputs_sidebar['input_fund']
        obj_received_data_times.type_of_request = outputs_sidebar['type_of_request']
        sidebar_date_to = obj_received_data_times.receive_data_sidebar_dashboard(
            call_times_select_all_fund_strategy_result_dates())
        return jsonify({'sidebar_date_to': sidebar_date_to})

    elif outputs_sidebar['type_of_request'] == 'charts_data_sidebar':
        obj_received_data_times.version_strategy = outputs_sidebar['inputs_version']
        obj_received_data_times.fund_name = outputs_sidebar['input_fund']
        obj_received_data_times.type_of_request = outputs_sidebar['type_of_request']
        sidebar_date_to = obj_received_data_times.receive_data_sidebar_dashboard(
            call_times_select_all_fund_strategy_result_dates())
        return jsonify({'sidebar_date_to': sidebar_date_to})

    return json.dumps({'status': 'OK'})


@app.route('/times_sidebar_dashboard',  methods=['GET', 'POST'])
def times_sidebar_dashboard():
    global obj_received_data_times
    form = InputsTimesModel()
    form_side_bar = SideBarDataForm()
    export_data_sidebar, sidebar_date_to = 'not_export_data_sidebar', ''

    if obj_received_data_times.type_of_request == 'export_data_sidebar':
        export_data_sidebar = 'export_data_sidebar'
        signals, returns, positions = call_times_proc_caller(fund_name=obj_received_data_times.fund_name_export,
                                                             version_strategy=obj_received_data_times.version_strategy_export,
                                                             date_to=obj_received_data_times.date_to,
                                                             date_to_sidebar=obj_received_data_times.date_to_export_sidebar)
        export_times_data_to_csv(obj_received_data_times.version_strategy, signals, returns, positions)

    signals, returns, positions = call_times_proc_caller(fund_name=obj_received_data_times.fund_name,
                                                         version_strategy=obj_received_data_times.version_strategy,
                                                         date_to=obj_received_data_times.date_to,
                                                         date_to_sidebar=obj_received_data_times.date_to_sidebar)

    obj_times_charts_data = ComputeDataDashboardTimes(signals=signals, returns=returns, positions=positions)
    obj_times_charts_data.strategy_weight = obj_received_data_times.strategy_weight

    template_data = main_compute_data_dashboard_times(obj_times_charts_data, start_date=None, end_date=None)

    return render_template('times_dashboard.html',
                           title='Dashboard',
                           form=form,
                           date_run=obj_received_data_times.date_to_sidebar.strftime('%d/%m/%Y'),
                           sidebar_date_to=sidebar_date_to,
                           export_data_sidebar=export_data_sidebar,
                           form_side_bar=form_side_bar,
                           fund_strategy=obj_received_data_times.fund_strategy_dict,
                           fund_list=form_side_bar.input_fund_name_times,
                           versions_list=form_side_bar.input_versions_times,
                           **template_data)


@app.route('/times_charts_dashboard',  methods=['GET', 'POST'])
def times_charts_dashboard():
    global obj_received_data_times
    form = InputsTimesModel()
    form_side_bar = SideBarDataForm()
    positions_chart = False
    export_data_sidebar = 'not_export_data_sidebar'
    position_1y_lst, positions, dates_pos, position_1y_per_asset = [], [], [], []

    signals, returns, positions = call_times_proc_caller(fund_name=obj_received_data_times.fund_name,
                                                         version_strategy=obj_received_data_times.version_strategy,
                                                         date_to=obj_received_data_times.date_to,
                                                         date_to_sidebar=obj_received_data_times.date_to_sidebar)
    obj_times_charts_data = ComputeDataDashboardTimes(signals=signals, returns=returns, positions=positions)
    obj_times_charts_data.strategy_weight = obj_received_data_times.strategy_weight

    if request.method == 'POST':
        if form.submit_ok_positions.data:
            positions_chart = True
            start_date, end_date = request.form['start_date_box_times'], request.form['end_date_box_times']
            position_1y, dates_pos, position_1y_per_asset, position_1y_lst = \
                obj_times_charts_data.compute_positions_position_1y_each_asset(start_date, end_date)

        elif request.form['submit_button'] == 'assets_positions':
            position_1y, dates_pos, position_1y_per_asset, position_1y_lst = \
                obj_times_charts_data.compute_positions_position_1y_each_asset(start_date=None, end_date=None)
            df_positions = obj_times_charts_data.convert_dict_to_dataframe(position_1y, dates_pos)
            export_times_positions_data_to_csv(df_positions)

    template_data = main_compute_data_dashboard_times(obj_times_charts_data, start_date=None, end_date=None)

    if positions_chart:
        template_data['positions'], template_data['dates_pos'], template_data['position_1y_per_asset'] = position_1y_lst, dates_pos, position_1y_per_asset

    return render_template('times_dashboard.html',
                           title='Dashboard',
                           form=form,
                           date_run=obj_received_data_times.date_to.strftime('%d/%m/%Y'),
                           export_data_sidebar=export_data_sidebar,
                           form_side_bar=form_side_bar,
                           fund_strategy=obj_received_data_times.fund_strategy_dict,
                           fund_list=form_side_bar.input_fund_name_times,
                           versions_list=form_side_bar.input_versions_times,
                           **template_data)


@app.route('/effect_dashboard',  methods=['GET', 'POST'])
def effect_dashboard():
    global obj_received_data_effect

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
    global obj_received_data_times
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
