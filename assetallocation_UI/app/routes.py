# Contains view functions for various URLs
import pandas as pd
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
@app.route('/home')
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
        print("username", username)
        print("password", password)

        if username != username_origin or password != password_origin:
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        else:
            track_id = randomIdentification()
            login_user(User(track_id))
            return redirect(url_for('protected_models'))
    # when the user click on the submit button without adding credentials
    return redirect(url_for('login'))


@app.route('/selectArpModels')
@login_required
def protected_models():
    return render_template('selectArpModels.html', title="Models")

# @app.route('/redirection_models')
# @login_required
# def redirection_models():
#     bar = create_plot()
#     return render_template('redirection_display.html', plot=bar)

@app.route('/times_display',  methods=['GET', 'POST'])
@login_required
def times():
    form = InputsTimesModel()

    if request.method == "POST":
        if request.form['submit_button'] == 'selectInputs':
            data = {
                    form.time_lag.name: form.time_lag.data,
                    form.leverage_type.name: form.leverage_type.data,
                    form.volatility_window.name: form.volatility_window.data,
                    form.sig1_short.name: form.sig1_short.data,
                    form.sig1_long.name: form.sig1_long.data,
                    form.sig2_short.name: form.sig2_short.data,
                    form.sig2_long.name: form.sig2_long.data,
                    form.sig3_short.name: form.sig3_short.data,
                    form.sig3_long.name: form.sig3_long.data,
                    form.frequency.name: form.frequency.data,
                    form.week_day.name: form.week_day.data
                  }

            strategy_inputs = pd.DataFrame(data, columns=[form.time_lag.name,
                                                          form.leverage_type.name,
                                                          form.volatility_window.name,
                                                          form.sig1_short.name,
                                                          form.sig1_long.name
                                                          form.sig2_short.name,
                                                          form.sig2_long.name,
                                                          form.sig3_short.name,
                                                          form.sig3_long.name,
                                                          form.frequency.name,
                                                          form.week_day.name
                                                        ])

            print("INPUTS INPUTS", form.time_lag.name)
        if request.form['submit_button'] == 'runTimesModel':
            print("run the model")

    return render_template('times_display.html', title="Times", form=form)

    # return render_template('times_display.html', title="Times", form=form, run_date=run[0])

@app.route('/times_overview')
@login_required
def times_overview():
    times_data = read_data_from_excel()

    signals, positions, performance_weekly, performance_ytd,\
        sum_positions_equities, sum_positions_bonds, sum_positions_fx,\
        sum_performance_weekly_equities, sum_performance_weekly_bonds, \
        sum_performance_weekly_fx, sum_performance_ytd_equities, \
        sum_performance_ytd_bonds, sum_performance_ytd_fx = data_table_times(times_data=times_data)

    positions_us_equities_sparklines, positions_eu_equities_sparklines, positions_jp_equities_sparklines,\
        positions_hk_equities_sparklines, positions_us_bonds_sparklines, positions_uk_bonds_sparklines, \
    positions_eu_bonds_sparklines, positions_ca_bonds_sparklines, positions_jpy_sparklines, \
    positions_eur_sparklines, positions_aud_sparklines, positions_cad_sparklines, positions_gbp_sparklines = data_sparklines_charts(times_data=times_data)

    return render_template('times_overview.html', title="Times",
                           sum_positions_equities=sum_positions_equities,
                           sum_positions_bonds=sum_positions_bonds,
                           sum_positions_fx=sum_positions_fx,
                           sum_performance_weekly_equities=sum_performance_weekly_equities,
                           sum_performance_weekly_bonds=sum_performance_weekly_bonds,
                           sum_performance_weekly_fx=sum_performance_weekly_fx,
                           sum_performance_ytd_equities=sum_performance_ytd_equities,
                           sum_performance_ytd_bonds=sum_performance_ytd_bonds,
                           sum_performance_ytd_fx=sum_performance_ytd_fx,
                           signals_us_equities=signals['US Equities'],
                           signals_eu_equities=signals['EU Equities'],
                           signals_jp_equities=signals['JP Equities'],
                           signals_hk_equities=signals['HK Equities'],
                           signals_us_bonds=signals['US 10y Bonds'],
                           signals_uk_bonds=signals['UK 10y Bonds'],
                           signals_eu_bonds=signals['Eu 10y Bonds'],
                           signals_ca_bonds=signals['CA 10y Bonds'],
                           signals_jpy=signals['JPY'],
                           signals_eur=signals['EUR'],
                           signals_aud=signals['AUD'],
                           signals_cad=signals['CAD'],
                           signals_gbp=signals['GBP'],

                           positions_us_equities=positions['US Equities.2'],
                           positions_eu_equities=positions['EU Equities.2'],
                           positions_jp_equities=positions['JP Equities.2'],
                           positions_hk_equities=positions['HK Equities.2'],
                           positions_us_bonds=positions['US 10y Bonds.2'],
                           positions_uk_bonds=positions['UK 10y Bonds.2'],
                           positions_eu_bonds=positions['Eu 10y Bonds.2'],
                           positions_ca_bonds=positions['CA 10y Bonds.2'],
                           positions_jpy=positions['JPY.2'],
                           positions_eur=positions['EUR.2'],
                           positions_aud=positions['AUD.2'],
                           positions_cad=positions['CAD.2'],
                           positions_gbp=positions['GBP.2'],

                           performance_us_equities=performance_weekly['US Equities.1'],
                           performance_eu_equities=performance_weekly['EU Equities.1'],
                           performance_jp_equities=performance_weekly['JP Equities.1'],
                           performance_hk_equities=performance_weekly['HK Equities.1'],
                           performance_us_bonds=performance_weekly['US 10y Bonds.1'],
                           performance_uk_bonds=performance_weekly['UK 10y Bonds.1'],
                           performance_eu_bonds=performance_weekly['Eu 10y Bonds.1'],
                           performance_ca_bonds=performance_weekly['CA 10y Bonds.1'],
                           performance_jpy=performance_weekly['JPY.1'],
                           performance_eur=performance_weekly['EUR.1'],
                           performance_aud=performance_weekly['AUD.1'],
                           performance_cad=performance_weekly['CAD.1'],
                           performance_gbp=performance_weekly['GBP.1'],

                           performance_ytd_us_equities=performance_ytd['US Equities.1'],
                           performance_ytd_eu_equities=performance_ytd['EU Equities.1'],
                           performance_ytd_jp_equities=performance_ytd['JP Equities.1'],
                           performance_ytd_hk_equities=performance_ytd['HK Equities.1'],
                           performance_ytd_us_bonds=performance_ytd['US 10y Bonds.1'],
                           performance_ytd_uk_bonds=performance_ytd['UK 10y Bonds.1'],
                           performance_ytd_eu_bonds=performance_ytd['Eu 10y Bonds.1'],
                           performance_ytd_ca_bonds=performance_ytd['CA 10y Bonds.1'],
                           performance_ytd_jpy=performance_ytd['JPY.1'],
                           performance_ytd_eur=performance_ytd['EUR.1'],
                           performance_ytd_aud=performance_ytd['AUD.1'],
                           performance_ytd_cad=performance_ytd['CAD.1'],
                           performance_ytd_gbp=performance_ytd['GBP.1'],

                           us_equities_sparklines=positions_us_equities_sparklines,
                           positions_eu_equities_sparklines=positions_eu_equities_sparklines,
                           positions_jp_equities_sparklines=positions_jp_equities_sparklines,
                           positions_hk_equities_sparklines=positions_hk_equities_sparklines,
                           positions_us_bonds_sparklines=positions_us_bonds_sparklines,
                           positions_uk_bonds_sparklines=positions_uk_bonds_sparklines,
                           positions_eu_bonds_sparklines=positions_eu_bonds_sparklines,
                           positions_ca_bonds_sparklines=positions_ca_bonds_sparklines,
                           positions_jpy_sparklines=positions_jpy_sparklines,
                           positions_eur_sparklines=positions_eur_sparklines,
                           positions_aud_sparklines=positions_aud_sparklines,
                           positions_cad_sparklines=positions_cad_sparklines,
                           positions_gbp_sparklines=positions_gbp_sparklines


                           )


@app.route('/times_dashboard', methods=['GET', 'POST'])
@login_required
def times_dashboard():
    form = ExportDataForm()
    times_data = read_data_from_excel()

    positions_us_equities, positions_eu_equities, positions_jp_equities, positions_hk_equities, positions_us_bonds, \
    positions_uk_bonds, positions_eu_bonds, positions_ca_bonds, positions_jpy, positions_eur, positions_aud, \
    positions_cad, positions_gbp = data_allocation_over_time_chart(times_data)

    performance_total, performance_gbp, performance_jpy, performance_eur, performance_aud, \
    performance_cad, performance_dates = data_performance_since_inception_chart(times_data)

    signals = data_table_times(times_data=times_data)

    print(type(performance_total))
    if request.method == "POST":
        if request.form['submit_button'] == 'selectInputToExport':
            print(form.start_date.data)
            print(form.end_date.data)
        elif request.form['submit_button'] == 'selectInputOk':
            print(form.inputs.data)
        elif request.form['submit_button'] == 'selectDatesChart':
            print(form.start_date_chart.data) #we need to separate each button date for each, otherwise, they will be connected to each other

    return render_template('new_dashboard_js.html', form=form,
                           positions_us_equities=positions_us_equities,
                           positions_eu_equities=positions_eu_equities,
                           positions_jp_equities=positions_jp_equities,
                           positions_hk_equities=positions_hk_equities,
                           positions_us_bonds=positions_us_bonds,
                           positions_uk_bonds=positions_uk_bonds,
                           positions_eu_bonds=positions_eu_bonds,
                           positions_ca_bonds=positions_ca_bonds,
                           positions_jpy=positions_jpy,
                           positions_eur=positions_eur,
                           positions_aud=positions_aud,
                           positions_cad=positions_cad,
                           positions_gbp=positions_gbp,
                           performance_total=performance_total,
                           performance_gbp=performance_gbp,
                           performance_jpy=performance_jpy,
                           performance_eur=performance_eur,
                           performance_aud=performance_aud,
                           performance_cad=performance_cad,
                           performance_dates=performance_dates,
                           )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


