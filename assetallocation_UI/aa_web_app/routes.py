import json

from flask import render_template
from flask import request

from assetallocation_UI.aa_web_app import app
from assetallocation_UI.aa_web_app.forms import InputsTimesModel, InputsEffectStrategy
from assetallocation_arp.arp_strategies import run_effect_strategy
from assetallocation_UI.aa_web_app.get_data_effect import ReceivedDataEffect

obj_received_data_effect = ReceivedDataEffect()


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
@app.route('/times_dashboard',  methods=['GET', 'POST'])
def times_dashboard():
    # form = ExportDataForm()
    form = InputsTimesModel()
    # template_data = main_data('f1', 399)

    return render_template('times_dashboard.html', form=form, title='Dashboard')


@app.route('/effect_dashboard',  methods=['GET', 'POST'])
def effect_dashboard():
    form = InputsTimesModel()
    effect_data_form = obj_received_data_effect.effect_data_form
    effect_outputs = obj_received_data_effect.effect_outputs
    write_logs = obj_received_data_effect.write_logs

    return render_template('effect_dashboard.html', form=form, effect_outputs=effect_outputs, write_logs=write_logs,
                           effect_data_form=effect_data_form, title='Dashboard')


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
    # todo store data in db with an id + concatenate id in the redirect url + load data in tables using id
    #  ex: "/some_url?x=1&y=2"
    # todo class instance

    form_data = request.form['form_data'].split('&')
    effect_form = obj_received_data_effect.received_data_effect(form_data)

    print(request.form['json_data'])

    obj_received_data_effect.call_run_effect(effect_form, assets_inputs_effect=json.loads(request.form['json_data']))

    return json.dumps({'status': 'OK', 'effect_data': effect_form})


@app.route('/risk_returns', methods=['GET', 'POST'])
def risk_returns():
    effect_outputs = obj_received_data_effect.effect_outputs

    print(effect_outputs['risk_returns'])

    print()
    return render_template('risk_returns_template.html', title='Risk_Returns_overall', effect_outputs=effect_outputs)


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
