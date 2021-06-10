import os
import json
from flask import render_template
from flask import request, redirect, url_for, jsonify, make_response

from assetallocation_UI.aa_web_app import app

from assetallocation_UI.aa_web_app.service.fund import get_fund_names
from assetallocation_arp.common_libraries.dal_enums.strategy import Name
from assetallocation_UI.aa_web_app.service.formatter import format_versions
from assetallocation_UI.aa_web_app.service.strategy import get_strategy_versions
from assetallocation_UI.aa_web_app.forms_times import InputsTimesModel, SideBarDataForm
from assetallocation_UI.aa_web_app.data_import.process_existing_data_times import ProcessExistingDataTimes
from assetallocation_UI.aa_web_app.data_import.compute_data_dashboard_times import ComputeDataDashboardTimes
from assetallocation_UI.aa_web_app.data_import.main_compute_data_dashboard_times import main_compute_data_dashboard_times
from assetallocation_UI.aa_web_app.data_import.call_times_proc_caller import call_times_proc_caller, \
    call_times_select_all_fund_strategy_result_dates
from assetallocation_UI.aa_web_app.data_import.download_data_strategy_to_domino import export_times_data_to_csv, \
    export_times_positions_data_to_csv


from assetallocation_UI.aa_web_app.data_import.run_new_strategy_times import RunNewStrategyTimes
from assetallocation_UI.aa_web_app.data_import.run_existing_strategy_times import run_existing_strategy
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

    obj_process_existing_data = ProcessExistingDataTimes()

    if request.method == 'POST':

        try:
            if request.form['submit_button'] == 'new-version':
                run_model_page = 'run_new_version'
                asset_tickers_names_subcategories = select_tickers()

        except:

            json_data = json.loads(request.form['json_data'])

            # Check if the selected date is in the database
            is_date_in_db = obj_process_existing_data.check_in_date_to_existing_version(json_data['fund_name'],
                                                                                        json_data['strategy_version'],
                                                                                        json_data['date_to'])
            if is_date_in_db:
                message = 'pop_up_message'

            else:
                message = 'run_existing_version'

            assets, inputs_existing_versions_times = obj_process_existing_data.receive_data_existing_versions(
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


@app.route('/times_strategy_existing_version/<version_selected>/<assets>/<message>/<inputs_existing_versions>/'
           '<userNameValue>', methods=['GET', 'POST'])
def times_strategy_existing_version(version_selected, assets, message, inputs_existing_versions, userNameValue):
    existing_versions_from_db = format_versions(get_strategy_versions(Name.times))
    existing_funds_from_db = get_fund_names()

    if message == 'call_run_existing_strategy':
        inputs = json.loads(inputs_existing_versions.split('\\')[0].replace("\'", "\""))
        print('RUN EXISTING VERSION')
        print(inputs, flush=True)
        print(userNameValue, flush=True)
        fund_strategy = run_existing_strategy(inputs, userNameValue)

        print("CALL THE DASHBOARD")
        print(fund_strategy.fund_name)
        print(fund_strategy.strategy_version)
        print(inputs['input_date_to_times'])
        return redirect(url_for('times_charts_dashboard',
                                fund_name=fund_strategy.fund_name,
                                strategy_version=fund_strategy.strategy_version,
                                date_to=inputs['input_date_to_times'],
                                **request.args))
    else:
        obj_process_existing_data = ProcessExistingDataTimes()

        asset_tmp, inputs_tmp = obj_process_existing_data.preprocess_strategy_existing_data(assets,
                                                                                            inputs_existing_versions)

    return render_template('times_template.html',
                           title='TimesPage',
                           userNameValue=userNameValue,
                           version_selected=version_selected,
                           existing_funds_from_db=existing_funds_from_db,
                           run_model_page=message,
                           assets=asset_tmp,
                           existing_versions_from_db=existing_versions_from_db,
                           inputs_versions=inputs_tmp)


@app.route('/receive_assets_from_jquery_table_times_strategy_page', methods=['POST'])
def receive_assets_from_jquery_table_times_strategy_page():

    json_data = json.loads(request.form['json_data'])

    name, subcategory = select_names_subcategories(json_data['input_signal_ticker_from_times'])
    return jsonify({'name': name, 'subcategory': subcategory})


@app.route('/call_run_times_new_strategy', methods=['POST'])
def call_run_times_new_strategy():
    form_data = request.form['form_data'].split('&')
    json_data = json.loads(request.form['json_data'])
    form_data.append('input_version_name=' + json_data['input_version_name_strategy'])

    fund_name = request.form['fundNameValue']
    strategy_weight = float(request.form['strategyWeightValue'])
    user_name = request.form['userNameValue']
    strategy_description = json_data["input_version_name_strategy"]

    obj_call_run_times = RunNewStrategyTimes(fund_name, strategy_weight, user_name, strategy_description)
    times_form = obj_call_run_times.process_data_times(form_data)
    fund_strategy, date_to = obj_call_run_times.run_times(json_data, times_form)

    return jsonify({'strategy_version': fund_strategy.strategy_version, 'date_to': date_to.replace('/', 'S')})


@app.route('/receive_sidebar_data_times_form', methods=['POST'])
def receive_sidebar_data_times_form():
    outputs_sidebar = json.loads(request.form['jsonData'])

    if outputs_sidebar['type_of_request'] == 'date_to_export_data_sidebar':

        signals, returns, positions = call_times_proc_caller(fund_name=outputs_sidebar['input_fund'],
                                                             strategy_version=int(outputs_sidebar['inputs_version']),
                                                             date_to=outputs_sidebar['inputs_date_to'])
        export_times_data_to_csv(int(outputs_sidebar['inputs_version']),
                                 signals, returns, positions,
                                 outputs_sidebar['input_fund'],
                                 outputs_sidebar['inputs_date_to'])

        return json.dumps({'status': 'OK'})

    elif outputs_sidebar['type_of_request'] == 'export_data_sidebar':
        version_strategy_export = outputs_sidebar['inputs_version']
        fund_name_export = outputs_sidebar['input_fund']
        date_to = call_times_select_all_fund_strategy_result_dates(fund_name_export, version_strategy_export)
        return jsonify({'sidebar_date_to': date_to})

    elif outputs_sidebar['type_of_request'] == 'charts_data_sidebar':
        fund_name = outputs_sidebar['input_fund']
        version_strategy = outputs_sidebar['inputs_version']
        date_to = call_times_select_all_fund_strategy_result_dates(fund_name, version_strategy)
        
        return jsonify({'sidebar_date_to': date_to,
                        'version_strategy': version_strategy,
                        'fund_name': fund_name})

    elif outputs_sidebar['type_of_request'] == 'date_charts_sidebar':

        return json.dumps({'status': 'OK'})


@app.route('/times_charts_dashboard/<fund_name>/<strategy_version>/<date_to>', defaults={'start_date_sidebar': None,
                                                                                         'type_of_request': None},
           methods=['GET', 'POST'])
@app.route('/times_charts_dashboard/<fund_name>/<strategy_version>/<date_to>/<start_date_sidebar>/<type_of_request>',
           methods=['GET', 'POST'])
def times_charts_dashboard(fund_name, strategy_version, date_to, start_date_sidebar, type_of_request):
    form = InputsTimesModel()
    form_side_bar = SideBarDataForm()
    export_data_sidebar, pop_up_success_domino = 'not_export_data_sidebar', ''

    print(f"----- fund_name ------- = {fund_name}", flush=True)
    print(f"----- strategy_version ----- = {strategy_version}", flush=True)
    print(f"----- date_to ----- = {date_to}", flush=True)

    date_to = date_to.replace('S', '/')

    signals, returns, positions = call_times_proc_caller(fund_name=fund_name,
                                                         strategy_version=int(strategy_version),
                                                         date_to=date_to)

    obj_times_charts_data = ComputeDataDashboardTimes(signals=signals, returns=returns, positions=positions)

    if type_of_request == 'download_asset_allocations_charts':
            position_1y, dates_pos, position_1y_per_asset, position_1y_lst = \
                obj_times_charts_data.compute_positions_position_1y_each_asset(start_date=None, end_date=None)
            df_positions = obj_times_charts_data.convert_dict_to_dataframe(position_1y, dates_pos)
            export_times_positions_data_to_csv(df_positions, fund_name, strategy_version)
            pop_up_success_domino = 'pop_up_success_domino'

    elif type_of_request == 'export_charts_data':
        pop_up_success_domino = 'pop_up_success_domino'

    if type_of_request == 'asset_alloc_charts':
        start_date = start_date_sidebar.replace('S', '/')
    else:
        start_date = '10/11/2019'

    template_data = main_compute_data_dashboard_times(obj_times_charts_data, start_date=start_date, end_date=date_to)

    return render_template('times_dashboard.html',
                           title='Dashboard',
                           form=form,
                           date_run=date_to,
                           export_data_sidebar=export_data_sidebar,
                           form_side_bar=form_side_bar,
                           fund_strategy={'fund': fund_name, 'strategy_version': strategy_version, 'date_to': date_to,
                                          'date_to_S':  date_to.replace('/', 'S')},
                           fund_list=form_side_bar.input_fund_name_times,
                           versions_list=form_side_bar.input_versions_times,
                           pop_up_success_domino=pop_up_success_domino,
                           **template_data)


@app.route('/asset_allocations_charts_success', methods=['POST'])
def asset_allocations_charts_success():
    return json.dumps({'status': 'OK'})

