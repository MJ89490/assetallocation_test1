import os
import json
from flask import render_template, session
from flask import request, redirect, url_for, jsonify, make_response

from assetallocation_UI.aa_web_app import app

from assetallocation_UI.aa_web_app.service.fund import get_fund_names
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
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


# obj_received_data_times = ReceiveDataTimes()
# obj_received_data_effect = ProcessDataEffect()

from assetallocation_UI.aa_web_app.data_import.call_run_times import CallRunTimes
from assetallocation_UI.aa_web_app.data_import.retrieve_tickers_from_db_times import select_tickers, \
    select_names_subcategories


@app.route('/',  methods=['GET'])
def home():
    r = make_response(render_template('home.html', title='HomePage'))
    if os.sys.platform == 'win32':
        r.set_cookie(key='username', value=os.environ.get('USERNAME'), max_age=None)
    return r


@app.route('/times_strategy', methods=['GET', 'POST'])
def times_strategy():
    run_model_page = 'not_run_model'
    asset_tickers_names_subcategories = []
    existing_versions_from_db = format_versions(get_strategy_versions(Name.times))
    existing_funds_from_db = get_fund_names()

    obj_received_data_times = ReceiveDataTimes()

    if request.method == 'POST':

        try:
            if request.form['submit_button'] == 'new-version':
                run_model_page = 'run_new_version'
                asset_tickers_names_subcategories = select_tickers()

        except:

            json_data = json.loads(request.form['json_data'])

            # Check if the selected date is in the database
            is_date_in_db = obj_received_data_times.check_in_date_to_existing_version(json_data['fund_name'],
                                                                                      json_data['strategy_version'],
                                                                                      json_data['date_to'])
            if is_date_in_db:
                message = 'pop_up_message'

            else:
                message = 'run_existing_version'

            assets, inputs_existing_versions_times = obj_received_data_times.receive_data_existing_versions(
                json_data['fund_name'],
                json_data['strategy_version'],
                json_data['strategy_weight_user'],
                json_data['date_to'])

            return jsonify({'message': message,
                            'version_selected':  json_data['strategy_version'],
                            'assets': assets,
                            'inputs_existing_versions_times': inputs_existing_versions_times})

    return render_template('times_template.html',
                           title='TimesPage',
                           asset_tickers_names_subcategories=asset_tickers_names_subcategories,
                           existing_funds_from_db=existing_funds_from_db,
                           run_model_page=run_model_page,
                           existing_versions_from_db=existing_versions_from_db)


@app.route('/times_strategy_existing_version/<version_selected>/<assets>/<message>/<inputs_existing_versions_times>/'
           '<userNameValue>', methods=['GET', 'POST'])
def times_strategy_existing_version(version_selected, assets, message, inputs_existing_versions_times, userNameValue):
    existing_versions_from_db = format_versions(get_strategy_versions(Name.times))
    existing_funds_from_db = get_fund_names()

    if message == 'call_run_existing_strategy':
        obj_received_data_times = ReceiveDataTimes()
        inputs = json.loads(inputs_existing_versions_times.split('\\')[0].replace("\'", "\""))
        fund_strategy = obj_received_data_times.run_existing_strategy(inputs, userNameValue)
        return redirect(url_for('times_charts_dashboard',
                                fund_name=fund_strategy.fund_name,
                                strategy_version=fund_strategy.strategy_version,
                                date_to=inputs['input_date_to_times'],
                                **request.args))
    else:
        # TODO MOVE TO FCT
        assets_split = assets.split(',')
        asset_tmp = []

        for val in range(0, len(assets_split), 5):
            tmp = assets_split[val:val + 5]
            asset_tmp.append(tmp)

        inputs_split = inputs_existing_versions_times.split(',')
        inputs_tmp = {}

        for val in range(0, len(inputs_split), 2):
            tmp = inputs_split[val: val + 2]
            inputs_tmp[tmp[0]] = tmp[1]

    return render_template('times_template.html',
                           title='TimesPage',
                           userNameValue=userNameValue,
                           version_selected=version_selected,
                           existing_funds_from_db=existing_funds_from_db,
                           run_model_page=message,
                           assets=asset_tmp,
                           existing_versions_from_db=existing_versions_from_db,
                           inputs_versions=inputs_tmp)


@app.route('/receive_data_from_times_strategy_page', methods=['POST'])
def receive_data_from_times_strategy_page():

    json_data = json.loads(request.form['json_data'])
    try:
        obj_received_data_times.type_of_request = json_data['run_existing-version']
    except KeyError:
        pass

    if json_data['type_of_request'] == 'selected_ticker':
        obj_received_data_times.type_of_request = json_data['type_of_request']
        name, subcategory = select_names_subcategories(json_data['input_signal_ticker_from_times'])
        return jsonify({'name': name, 'subcategory': subcategory})

    return json.dumps({'status': 'OK'})


@app.route('/receive_data_from_times_strategy_form', methods=['POST'])
def receive_data_from_times_strategy_form():
    form_data = request.form['form_data'].split('&')
    json_data = json.loads(request.form['json_data'])
    form_data.append('input_version_name=' + json_data['input_version_name_strategy'])

    fund_name = request.form['fundNameValue']
    strategy_weight = float(request.form['strategyWeightValue'])
    user_name = request.form['userNameValue']
    strategy_description = json_data["input_version_name_strategy"]

    obj_call_run_times = CallRunTimes(fund_name, strategy_weight, user_name, strategy_description)
    times_form = obj_call_run_times.process_data_times(form_data)
    fund_strategy, date_to = obj_call_run_times.call_run_times(json_data, times_form)

    return jsonify({'strategy_version': fund_strategy.strategy_version, 'date_to': date_to.replace('/', 'S')})


@app.route('/receive_sidebar_data_times_form', methods=['POST'])
def receive_sidebar_data_times_form():
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


@app.route('/times_charts_dashboard/<fund_name>/<strategy_version>/<date_to>',  methods=['GET', 'POST'])
def times_charts_dashboard(fund_name, strategy_version, date_to):
    form = InputsTimesModel()
    form_side_bar = SideBarDataForm()
    positions_chart = False
    export_data_sidebar = 'not_export_data_sidebar'
    position_1y_lst, positions, dates_pos, position_1y_per_asset = [], [], [], []

    print(f"----- fund_name ------- = {fund_name}", flush=True)
    print(f"----- strategy_version ----- = {strategy_version}", flush=True)
    print(f"----- date_to ----- = {date_to}", flush=True)

    date_to = date_to.replace('S', '/')

    signals, returns, positions = call_times_proc_caller(fund_name=fund_name,
                                                         strategy_version=int(strategy_version),
                                                         date_to=date_to,
                                                         date_to_sidebar=None)

    obj_times_charts_data = ComputeDataDashboardTimes(signals=signals, returns=returns, positions=positions)

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
        template_data['positions'], template_data['dates_pos'], template_data['position_1y_per_asset'] = position_1y_lst, \
                                                                                                         dates_pos, \
                                                                                                         position_1y_per_asset

    return render_template('times_dashboard.html',
                           title='Dashboard',
                           form=form,
                           date_run=date_to,
                           export_data_sidebar=export_data_sidebar,
                           form_side_bar=form_side_bar,
                           fund_strategy={'fund': fund_name, 'strategy_version': strategy_version, 'date_to': date_to},
                           fund_list=form_side_bar.input_fund_name_times,
                           versions_list=form_side_bar.input_versions_times,
                           **template_data)



