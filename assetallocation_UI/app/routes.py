# Contains view functions for various URLs
import pandas as pd
from assetallocation_arp.arp_strategies import run_model_from_web_interface, write_output_to_excel
from common_libraries.models_names import Models
from flask import render_template
from flask import flash
from flask import url_for
from flask import redirect
from flask import request
from app import app
from app.forms import LoginForm, ExportDataForm, InputsTimesModel
from .models import User

from flask_login import login_required
from flask_login import logout_user
from flask_login import login_user
from flask_login import current_user
from flask import g

from .userIdentification import randomIdentification
from .import_data_from_excel import read_data_from_excel, data_allocation_over_time_chart, \
    data_performance_since_inception_chart, data_table_times, data_sparklines_charts


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/hom')
def home():
    return render_template('home.html', title='HomePage')


@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', title='LoginPage', form=form)


@app.route('/login', methods=['POST'])
def login_post():
    username_origin = "database"
    password_origin = "1234*"
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username != username_origin or password != password_origin or username == ' ' or password == ' ':
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        else:
            track_id = randomIdentification()
            login_user(User(track_id))
            return redirect(url_for('home'))
    # when the user click on the submit button without adding credentials
    return redirect(url_for('login'))


@app.route('/times_page',  methods=['GET', 'POST'])
@login_required
def times_page():
    form = InputsTimesModel()

    global STRATEGY, ASSET_INPUTS, POSITIONING, R, SIGNALS, TIMES_INPUTS

    if request.method == "POST":
        # Selection of a model's version
        if request.form['submit_button'] == 'selectVersions':
            version_type = form.versions.data
            return render_template('times_page_new_version_layout.html', title="Times", form=form,
                                   version_type=version_type)
        # Run the model
        elif request.form['submit_button'] == 'runTimesModel':

            run_model = "run_times_model"
            run_model_ok = "run_times_model_ok"

            try:
                #handling data: another file (file data)
                data = {                                                        #todo créer une fct pour ces données
                            form.time_lag.name: [int(form.time_lag.data)],
                            form.leverage_type.name: [form.leverage_type.data],
                            form.volatility_window.name: [int(form.volatility_window.data)],
                            form.sig1_short.name: [int(form.sig1_short.data)],
                            form.sig1_long.name: [int(form.sig1_long.data)],
                            form.sig2_short.name: [int(form.sig2_short.data)],
                            form.sig2_long.name: [int(form.sig2_long.data)],
                            form.sig3_short.name: [int(form.sig3_short.data)],
                            form.sig3_long.name: [int(form.sig3_long.data)],
                            form.frequency.name: [form.frequency.data],
                            form.week_day.name: [form.week_day.data]
                          }
            except ValueError:
                message = "error parameters"
                return render_template('times_page_new_version_layout.html',
                                       title="Times", form=form, run_model=run_model, message=message)

            strategy_inputs = pd.DataFrame(data, columns=[form.time_lag.name,
                                                              form.leverage_type.name,
                                                              form.volatility_window.name,
                                                              form.sig1_short.name,
                                                              form.sig1_long.name,
                                                              form.sig2_short.name,
                                                              form.sig2_long.name,
                                                              form.sig3_short.name,
                                                              form.sig3_long.name,
                                                              form.frequency.name,
                                                              form.week_day.name
                                                              ])
            STRATEGY = strategy_inputs
            ASSET_INPUTS, POSITIONING, R, SIGNALS, TIMES_INPUTS = run_model_from_web_interface(model_type=Models.times.name)

            return render_template('times_page_new_version_layout.html', title="Times", form=form, run_model=run_model, run_model_ok=run_model_ok)

        elif request.form['submit_button'] == 'selectTimesPath':
            save = "save"
            save_file = "save_file"
            name_of_file = form.name_file_times.data + ".xls"
            path_excel = "C:\\Users\\AJ89720\\PycharmProjects" #todo change the default location later
            path_excel_times = path_excel + "\\" + name_of_file

            if form.save_excel_outputs.data is True:
                write_output_to_excel(model_outputs={Models.times.name:
                                                    (ASSET_INPUTS, POSITIONING, R, SIGNALS, TIMES_INPUTS)},
                                      path_excel_times=path_excel_times)

            return render_template('times_page_new_version_layout.html', title="Times", form=form, save=save, save_file=save_file)

    return render_template('times_page.html', title="Times", form=form)


@app.route('/times_dashboard', methods=['GET', 'POST'])
@login_required
def times_dashboard():
    form = ExportDataForm()

    from app.data_import.main_import_data import main

    # times_returns, times_positions, times_signals, times_signals_comp, times_positions_comp, times_returns_comp,\
    # sum_positions_equities, sum_positions_bonds, sum_positions_fx, sum_performance_weekly_equities, \
    # sum_performance_weekly_bonds, sum_performance_weekly_fx, sum_performance_ytd_equities, sum_performance_ytd_bonds, \
    # sum_performance_ytd_fx = run_times()

    times_returns, times_positions, times_signals = main()


    # template_data_new = {"times_returns": times_returns,
    #                      "times_positions": times_positions,
    #                      "times_signals": times_signals,
    #                      "times_signals_comp": times_signals_comp,
    #                      "times_positions_comp": times_positions_comp,
    #                      "times_returns_comp": times_returns_comp,
    #                      "sum_positions_equities": sum_positions_equities,
    #                      "sum_positions_bonds": sum_positions_bonds,
    #                      "sum_positions_fx": sum_positions_fx,
    #                      "sum_performance_weekly_equities": sum_performance_weekly_equities,
    #                      "sum_performance_weekly_bonds": sum_performance_weekly_bonds,
    #                      "sum_performance_weekly_fx": sum_performance_weekly_fx,
    #                      "sum_performance_ytd_equities": sum_performance_ytd_equities,
    #                      "sum_performance_ytd_bonds": sum_performance_ytd_bonds,
    #                      "sum_performance_ytd_fx": sum_performance_ytd_fx}
    template_data_new = {"times_returns": times_returns,
                         "times_positions": times_positions,
                         "times_signals": times_signals}


    # move the logic to another file
    times_data = read_data_from_excel()
    data_asset_alloc = data_allocation_over_time_chart(times_data=times_data)
    data_performance = data_performance_since_inception_chart(times_data=times_data)
    data_table = data_table_times(times_data=times_data)
    data_sparklines = data_sparklines_charts(times_data=times_data)
    template_data = {'asset_alloc': data_asset_alloc, 'performance': data_performance, 'table': data_table,
                     'sparklines': data_sparklines}

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
    return render_template('dashboard_new.html', form=form, m=m, **template_data, **template_data_new)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



