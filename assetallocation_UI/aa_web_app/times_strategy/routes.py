import json
from flask import redirect, url_for
from flask import Blueprint, render_template, request

from assetallocation_UI.aa_web_app.data_import.get_data_times import ReceivedDataTimes
from assetallocation_UI.aa_web_app.forms_times import InputsTimesModel, SideBarDataForm
from assetallocation_UI.aa_web_app.data_import.compute_charts_data import TimesChartsDataComputations
from assetallocation_UI.aa_web_app.data_import.main_import_data import run_times_charts_data_computations

obj_received_data_times = ReceivedDataTimes()

obj_times_charts_data = TimesChartsDataComputations()


times_strategy_bp = Blueprint('times_strategy_bp',
                              import_name=__name__,
                              template_folder='templates',
                              static_folder='static',
                              static_url_path='/aa_web_app/times_strategy/static')


@times_strategy_bp.route('/times_dashboard',  methods=['GET', 'POST'])
def times_dashboard():
    form = InputsTimesModel()
    form_side_bar = SideBarDataForm()
    positions_chart = False
    export_data_sidebar = 'not_export_data_sidebar'

    if request.method == 'POST':
        if form.submit_ok_positions.data:
            positions_chart = True
            start, end = request.form['start_date_box_times'], request.form['end_date_box_times']
            positions, dates_pos, names_pos = obj_times_charts_data.compute_positions_assets(start_date=start,
                                                                                             end_date=end)
        elif request.form['submit_button'] == 'dashboard':
            obj_received_data_times.receive_data_latest_version_dashboard()

        elif request.form['submit_button'] == 'assets_positions':
            obj_times_charts_data.export_times_positions_data_to_csv()

    else:
        if obj_received_data_times.type_of_request == 'export_data_sidebar':
            version = obj_received_data_times.version_strategy
            obj_times_charts_data.call_times_proc_caller(obj_received_data_times.fund_name, version)
            export_data_sidebar = 'export_data_sidebar'
            obj_times_charts_data.export_times_data_to_csv(version)

        obj_received_data_times.receive_data_selected_version_sidebar_dashboard()

    obj_times_charts_data.call_times_proc_caller(obj_received_data_times.fund_name,
                                                 obj_received_data_times.version_strategy,
                                                 date_to_sidebar=obj_received_data_times.date_to_sidebar)

    template_data = run_times_charts_data_computations(obj_times_charts_data,
                                                       obj_received_data_times.strategy_weight,
                                                       start_date_sum=None, start_date=None, end_date=None)
    if positions_chart:
        template_data['positions'], template_data['dates_pos'], template_data['names_pos'] = positions, dates_pos, names_pos

    return render_template('times_dashboard_old.html',
                           title='Dashboard',
                           form=form,
                           export_data_sidebar=export_data_sidebar,
                           form_side_bar=form_side_bar,
                           fund_strategy=obj_received_data_times.fund_strategy_dict,
                           fund_list=form_side_bar.input_fund_name_times,
                           versions_list=form_side_bar.input_versions_times,
                           **template_data)


@times_strategy_bp.route('/times_strategy', methods=['GET', 'POST'])
def times_strategy():
    form = InputsTimesModel()
    show_versions = 'show_versions_not_available'
    show_dashboard = 'show_dashboard_not_available'
    run_model_page = 'not_run_model'
    assets = []
    show_calendar, fund_selected = '', ''

    if request.method == 'POST':
        if request.form['submit_button'] == 'new-version':
            run_model_page = 'run_new_version'

        elif request.form['submit_button'] == 'run-strategy-existing-versions':
            obj_received_data_times.run_existing_strategy()

            return redirect(url_for('times_dashboard'))

    else:
        if obj_received_data_times.type_of_request == 'fund_selected':
            show_versions, show_dashboard = 'show_versions_available', 'show_dashboard'
            fund_selected = obj_received_data_times.fund_name

        elif obj_received_data_times.type_of_request == 'version_selected':
            show_versions, show_dashboard, show_calendar = 'show_versions_available', 'show_dashboard', 'show_calendar'

        elif obj_received_data_times.type_of_request == 'date_selected':
            assets = obj_received_data_times.receive_data_existing_versions(strategy_version=obj_received_data_times.version_strategy)
            run_model_page = 'run_existing_version'

    return render_template('times_template_old.html',
                           title='TimesPage',
                           form=form,
                           fund_selected=fund_selected,
                           existing_funds=form.existing_funds,
                           show_calendar=show_calendar,
                           show_versions=show_versions,
                           run_model_page=run_model_page,
                           show_dashboard=show_dashboard,
                           assets=assets,
                           versions_list=form.input_versions_times,
                           inputs_versions=obj_received_data_times.inputs_existing_versions_times)


@times_strategy_bp.route('/receive_data_from_times_strategy_page', methods=['POST'])
def receive_data_from_times_strategy_page():
    json_data = json.loads(request.form['json_data'])
    obj_received_data_times.type_of_request = json_data['type_of_request']
    global SHOW_CALENDAR

    if json_data['type_of_request'] == 'version_selected':
        obj_received_data_times.version_strategy = json_data['version']
        SHOW_CALENDAR = json_data['show_calendar']
    elif json_data['type_of_request'] == 'date_selected':
        obj_received_data_times.date_to = json_data['date_to']
    else:
        obj_received_data_times.fund_name = json_data['fund']

    return json.dumps({'status': 'OK'})


@times_strategy_bp.route('/received_data_times_form', methods=['POST'])
def received_data_times_form():
    form_data = request.form['form_data'].split('&')
    json_data = json.loads(request.form['json_data'])

    form_data.append('input_version_name=' + json_data['input_version_name_strategy'])

    obj_received_data_times.is_new_strategy = True
    obj_received_data_times.received_data_times(form_data)
    obj_received_data_times.call_run_times(json_data)
    return json.dumps({'status': 'OK'})


@times_strategy_bp.route('/receive_sidebar_data_times_form', methods=['POST'])
def receive_sidebar_data_times_form():
    outputs_sidebar = json.loads(request.form['json_data'])
    obj_received_data_times.version_strategy = outputs_sidebar['inputs_version']
    obj_received_data_times.fund_name = outputs_sidebar['input_fund']
    obj_received_data_times.type_of_request = outputs_sidebar['type_of_request']
    obj_received_data_times.date_to_sidebar = outputs_sidebar['inputs_date_to']
    return json.dumps({'status': 'OK'})