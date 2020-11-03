import os
import json

from flask import render_template
from flask import request

from assetallocation_UI.aa_web_app import app
from assetallocation_UI.aa_web_app.forms import InputsTimesModel, InputsEffectStrategy
from assetallocation_UI.aa_web_app.service.strategy import run_strategy
from assetallocation_UI.aa_web_app.data_import.main_import_data import main_data
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, TimesAssetInput, DayOfWeek


@app.route('/')
def home():
    return render_template('home.html', title='HomePage')


@app.route('/times_model',  methods=['GET', 'POST'])
def times_model():
    form = InputsTimesModel()
    run_model_page = 'run_model_page'

    if request.method == "POST":
        # TODO set a specific layout depending on the version!
        version_type = form.versions.data

        return render_template('times_model_mirror.html', form=form, title='TimesPage')

    return render_template('times_model.html', form=form, title='TimesPage', run_model_page=run_model_page)


# @app.route('/times_dashboard', defaults={'fund_name': None, 'times_version': None}, methods=['GET', 'POST'])
# @app.route('/times_dashboard/<string:fund_name>/<int:times_version>', methods=['GET', 'POST'])
# <<<<<<< HEAD
# @app.route('/times_dashboard',  methods=['GET', 'POST'])
# =======
# @app.route('/times_dashboard',  methods=['POST'])
# >>>>>>> feature/flask_UI_dal_integration_new_layout
# def times_dashboard():
#     # form = ExportDataForm()
#     form = InputsTimesModel()
#     # template_data = main_data('f1', 399)
#
#     return render_template('times_dashboard.html', form=form, title='Dashboard')


# @app.route('/receive_times_data', methods=['POST'])
# def receive_times_data():
#     form = InputsTimesModel()
#
#     if request.method == "POST":
#         t = request.get_json()
#         print(t)
#         fund_name = t['fund']
#         long_signals = list(map(float, [t['signalonelong'], t['signaltwolong'], t['signalthreelong']]))
#         short_signals = list(map(float, [t['signaloneshort'], t['signaltwoshort'], t['signalthreeshort']]))
#         times = Times(DayOfWeek[t['weekday'].upper()], t['frequency'].lower(), t['leverage'], long_signals,
#                       short_signals, int(t['lag']), int(t['volwindow']))
#
#         times.asset_inputs = [TimesAssetInput(int(i), j, k, float(l)) for i, j, k, l in
#                               zip(t['assetsLeverage'], t['assetsTicker'], t['assetsFutureTicker'], t['assetsCosts'])]
#
#         # TODO do not work with that line !!!!!
#         fund_strategy = run_strategy(fund_name, float(t['weight']), times, os.environ.get('USERNAME'), t['date'])
#
#         return json.dumps({'status': 'OK'})



@app.route('/effect_strategy_get', methods=['GET'])
def effect_strategy_get():
    form = InputsEffectStrategy(request.form)
    run_model_page = 'not_run_model_page'
    return render_template('effect_page.html', title='EffectPage', form=form, run_model_page=run_model_page)


@app.route('/effect_strategy_post', methods=['POST'])
def effect_strategy_post():
    form = InputsEffectStrategy(request.form)
    run_model_page = 'run_model_page'
    return render_template('effect_page.html', title='EffectPage', form=form, run_model_page=run_model_page)


@app.route('/received_data_effect_form', methods=['POST'])
def received_data_effect_form():
    effect_form = {}

    form_data = request.form['form_data'].split('&')

    for idx, val in enumerate(form_data):
        if idx > 1:
            effect_form[val.split('=', 1)[0]] = val.split('=', 1)[1]

    print(effect_form)
    print(request.form['json_data'])

    t = {'assetsNames': ['US Equities'], 'assetsTicker': ['SPXT Index'], 'assetsFutureTicker': ['SPXT Index'], 'assetsCosts': [0.0002], 'assetsLeverage': [1], 'fund': 'f1', 'date': '01/01/2000', 'weight': '1', 'lag': '1', 'leverage': 'v', 'volwindow': '3', 'frequency': 'weekly', 'weekday': 'Mon', 'signaloneshort': '15', 'signalonelong': '30', 'signaltwoshort': '15', 'signaltwolong': '30', 'signalthreeshort': '15', 'signalthreelong': '30'}
    fund_name = t['fund']
    long_signals = list(map(float, [t['signalonelong'], t['signaltwolong'], t['signalthreelong']]))
    short_signals = list(map(float, [t['signaloneshort'], t['signaltwoshort'], t['signalthreeshort']]))
    times = Times(DayOfWeek[t['weekday'].upper()], t['frequency'].lower(), t['leverage'], long_signals,
                  short_signals, int(t['lag']), int(t['volwindow']))

    times.asset_inputs = [TimesAssetInput(int(i), j, k, float(l)) for i, j, k, l in
                          zip(t['assetsLeverage'], t['assetsTicker'], t['assetsFutureTicker'], t['assetsCosts'])]

    # TODO do not work with that line !!!!!
    fund_strategy = run_strategy(fund_name, float(t['weight']), times, os.environ.get('USERNAME'), t['date'])

    return json.dumps({'status': 'OK'})


#     if request.method == "POST":
#         t = request.get_json()
#         fund_name = t['fund']
#         long_signals = list(map(float, [t['signalonelong'], t['signaltwolong'], t['signalthreelong']]))
#         short_signals = list(map(float, [t['signaloneshort'], t['signaltwoshort'], t['signalthreeshort']]))
#         times = Times(DayOfWeek[t['weekday'].upper()], t['frequency'].lower(), t['leverage'], long_signals,
#                       short_signals, int(t['lag']), int(t['volwindow']))
#         print('before times assets')
#         times.asset_inputs = [TimesAssetInput(int(i), j, k, float(l)) for i, j, k, l in
#                               zip(t['assetsLeverage'], t['assetsTicker'], t['assetsFutureTicker'], t['assetsCosts'])]
#         print('after times assets')
#         # TODO do not work with that line !!!!!
#         fund_strategy = run_strategy(fund_name, float(t['weight']), times, os.environ.get('USERNAME'), t['date'])
#         print('after fund strategy')
#         return json.dumps({'status': 'OK'})
# >>>>>>> feature/flask_UI_dal_integration_new_layout


# @app.route('/times_dashboard', defaults={'fund_name': None, 'times_version': None}, methods=['GET', 'POST'])
# @app.route('/times_dashboard/<string:fund_name>/<int:times_version>', methods=['GET', 'POST'])
# def times_dashboard(fund_name: str, times_version: int):
#     title = "Dashboard"
#     form = ExportDataForm()
#     template_data = main_data(fund_name, times_version)
#
#     m = ""
#     if request.method == "POST":
#
#         # Sidebar: charts export
#         if request.form['submit_button'] == 'selectChartsVersionsOk':
#             print(form.versions.data)
#         elif request.form['submit_button'] == 'selectChartsLeverageOk':
#             print(form.leverage.data)
#         elif request.form['submit_button'] == 'selectChartsSubmit':
#             print("Submit chats data")
#
#         # Sidebar: data export
#         if request.form['submit_button'] == 'selectVersionsOk':
#             print(form.versions.data)
#         elif request.form['submit_button'] == 'selectLeverageOk':
#                 print(form.leverage.data)
#         elif request.form['submit_button'] == 'selectInputsOk':
#             print(form.inputs.data)
#         elif request.form['submit_button'] == 'selectStartDateOk':
#             print(form.start_date_inputs.data)
#         elif request.form['submit_button'] == 'selectEndDateOk':
#             print(form.end_date_inputs.data)
#         elif request.form['submit_button'] == 'selectDataSubmit':
#             print("Submit data")
#
#         # Main: charts area
#         if request.form['submit_button'] == 'selectInputToExport':
#             if form.start_date_inputs.data > form.end_date_inputs.data:
#                 flash("Check the Start and End Date. They are incorrect.")
#             else:
#                 print("Take the data from the CACHE db")
#                 print(form.start_date_inputs.data)
#                 print(form.end_date_inputs.data)
#         elif request.form['submit_button'] == 'selectInputOk':
#             print(form.inputs.data)
#
#         elif request.form['submit_button'] == 'selectDatesChart0':
#             if form.start_date_chart0.data > form.end_date_chart0.data:
#                 m = "Check the Start and End Date. They are incorrect for the first chart."
#             else:
#                 print("Date chart 0")
#
#         elif request.form['submit_button'] == 'selectDatesChart1':
#             if form.start_date_chart1.data > form.end_date_chart1.data:
#                 m = "Check the Start and End Date. They are incorrect for this second chart."
#             else:
#                 print("Date chart 1")
#
#         elif request.form['submit_button'] == 'selectDatesChart2':
#             if form.start_date_chart2.data > form.end_date_chart2.data:
#                 m = "Check the Start and End Date. They are incorrect for this third chart."
#             else:
#                 print("Date chart 2")
#
#         elif request.form['submit_button'] == 'selectDatesChart3':
#             if form.start_date_chart3.data > form.end_date_chart3.data:
#                 m = "Check the Start and End Date. They are incorrect for this fourth chart."
#             else:
#                 print("Date chart 3")
#
#         elif request.form['submit_button'] == 'selectDatesChart4':
#             if form.start_date_chart4.data > form.end_date_chart4.data:
#                 m = "Check the Start and End Date. They are incorrect for this fifth chart."
#             else:
#                 print("Date chart 4")
#
#         elif request.form['submit_button'] == 'selectDatesChart5':
#             if form.start_date_chart5.data > form.end_date_chart5.data:
#                 m = "Check the Start and End Date. They are incorrect for this sixth chart."
#             else:
#                 print("Date chart 5")
#
#         elif request.form['submit_button'] == 'selectDatesChart6':
#             if form.start_date_chart6.data > form.end_date_chart6.data:
#                 m = "Check the Start and End Date. They are incorrect for this seventh chart."
#             else:
#                 print("Date chart 6")
#
#         elif request.form['submit_button'] == 'selectDataChart0':
#             print('data data data')
#
#     # put the data in dict or create a class to handle the data nicer (later with the db?)
#     return render_template('dashboard_new.html', title=title, form=form, m=m, **template_data)
