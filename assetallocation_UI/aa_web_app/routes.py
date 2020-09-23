# Contains view functions for various URLs
from assetallocation_UI.aa_web_app.data_import.main_import_data import main_data
from assetallocation_UI.aa_web_app.data_import.main_import_data_from_form import get_times_inputs
from flask import render_template
from flask import flash
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime

from assetallocation_UI.aa_web_app import app
from assetallocation_UI.aa_web_app.forms import LoginForm, ExportDataForm, InputsTimesModel
# from .models import User
from assetallocation_UI.aa_web_app.service.strategy import run_strategy
from assetallocation_arp.data_etl.dal.data_models.strategy import TimesAssetInput

import os
# from flask_login import login_user
# from flask_login import current_user
from flask import g

from .userIdentification import random_identification

# TODO mock content and test each route to see if they are ok
# TODO create blueprints to avoid having single routes
# TODO check with Jess for dashboard regarding inputs in the sidebar + see with her how it works
# TODO change the names in asset_inputs.py (name convention)

@app.route('/')
def home():
    return render_template('home_new.html', title='HomePage')


@app.route('/times_model',  methods=['GET', 'POST'])
def times_model():
    form = InputsTimesModel()
    run_model_page = 'run_model_page'

    if request.method == "POST":
        # TODO set a specific layout depending on the version!
        version_type = form.versions.data

        return render_template('times_model_mirror.html', form=form, title='TimesPage')

    return render_template('times_model.html', form=form, title='TimesPage', run_model_page=run_model_page)


@app.route('/received_data_run_model',  methods=['GET', 'POST'])
def received_data_run_model():
    form = InputsTimesModel()
    if request.method == "POST":
        times_data = request.data
        print(times_data)
        # -------- All the data are in the times_data (form + ag grd) in a dict --------
        # fund_name, strategy_weight, times
        # date_from = datetime(2019, 12, 1)
        # times.asset_inputs = [TimesAssetInput(3, 'RX1 A:00_0_R Comdty', 'RX1 A:00_0_R Comdty', 0.0002)]
        # fund_strategy = run_strategy(fund_name, strategy_weight, times, os.environ.get('USERNAME'), date_from)
        # TODO should redirect to dashboard after running of a model, with the strategy_version
        # return redirect(url_for('times_dashboard', fund_name=fund_name, times_version=fund_strategy.strategy_version))
        return render_template('times_model_mirror.html', form=form, title='TimesPage')
    return render_template('times_model_mirror.html', form=form, title='TimesPage')


# @app.route('/times_dashboard',  methods=['GET', 'POST'])
# def times_dashboard():
#     form = InputsTimesModel()
#     # form = ExportDataForm()
#     # template_data = main_data('f1', 1)
#
#     return render_template('times_dashboard.html', form=form, title='Dashboard')


@app.route('/times_dashboard', defaults={'fund_name': None, 'times_version': None}, methods=['GET', 'POST'])
@app.route('/times_dashboard/<string:fund_name>/<int:times_version>', methods=['GET', 'POST'])
def times_dashboard(fund_name: str, times_version: int):
    title = "Dashboard"
    form = ExportDataForm()
    template_data = main_data(fund_name, times_version)

    m = ""
    if request.method == "POST":

        # Sidebar: charts export
        if request.form['submit_button'] == 'selectChartsVersionsOk':
            print(form.versions.data)
        elif request.form['submit_button'] == 'selectChartsLeverageOk':
            print(form.leverage.data)
        elif request.form['submit_button'] == 'selectChartsSubmit':
            print("Submit chats data")

        # Sidebar: data export
        if request.form['submit_button'] == 'selectVersionsOk':
            print(form.versions.data)
        elif request.form['submit_button'] == 'selectLeverageOk':
                print(form.leverage.data)
        elif request.form['submit_button'] == 'selectInputsOk':
            print(form.inputs.data)
        elif request.form['submit_button'] == 'selectStartDateOk':
            print(form.start_date_inputs.data)
        elif request.form['submit_button'] == 'selectEndDateOk':
            print(form.end_date_inputs.data)
        elif request.form['submit_button'] == 'selectDataSubmit':
            print("Submit data")

        # Main: charts area
        if request.form['submit_button'] == 'selectInputToExport':
            if form.start_date_inputs.data > form.end_date_inputs.data:
                flash("Check the Start and End Date. They are incorrect.")
            else:
                print("Take the data from the CACHE db")
                print(form.start_date_inputs.data)
                print(form.end_date_inputs.data)
        elif request.form['submit_button'] == 'selectInputOk':
            print(form.inputs.data)

        elif request.form['submit_button'] == 'selectDatesChart0':
            if form.start_date_chart0.data > form.end_date_chart0.data:
                m = "Check the Start and End Date. They are incorrect for the first chart."
            else:
                print("Date chart 0")

        elif request.form['submit_button'] == 'selectDatesChart1':
            if form.start_date_chart1.data > form.end_date_chart1.data:
                m = "Check the Start and End Date. They are incorrect for this second chart."
            else:
                print("Date chart 1")

        elif request.form['submit_button'] == 'selectDatesChart2':
            if form.start_date_chart2.data > form.end_date_chart2.data:
                m = "Check the Start and End Date. They are incorrect for this third chart."
            else:
                print("Date chart 2")

        elif request.form['submit_button'] == 'selectDatesChart3':
            if form.start_date_chart3.data > form.end_date_chart3.data:
                m = "Check the Start and End Date. They are incorrect for this fourth chart."
            else:
                print("Date chart 3")

        elif request.form['submit_button'] == 'selectDatesChart4':
            if form.start_date_chart4.data > form.end_date_chart4.data:
                m = "Check the Start and End Date. They are incorrect for this fifth chart."
            else:
                print("Date chart 4")

        elif request.form['submit_button'] == 'selectDatesChart5':
            if form.start_date_chart5.data > form.end_date_chart5.data:
                m = "Check the Start and End Date. They are incorrect for this sixth chart."
            else:
                print("Date chart 5")

        elif request.form['submit_button'] == 'selectDatesChart6':
            if form.start_date_chart6.data > form.end_date_chart6.data:
                m = "Check the Start and End Date. They are incorrect for this seventh chart."
            else:
                print("Date chart 6")

        elif request.form['submit_button'] == 'selectDataChart0':
            print('data data data')

    # put the data in dict or create a class to handle the data nicer (later with the db?)
    return render_template('dashboard_new.html', title=title, form=form, m=m, **template_data)
