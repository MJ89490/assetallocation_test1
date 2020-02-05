# Contains view functions for various URLs
from flask import render_template
from flask import flash
from flask import url_for
from flask import redirect
from flask import request
from app import app
from app.forms import LoginForm, ExportDataForm
from .models import User

from flask_login import login_required
from flask_login import logout_user
from flask_login import login_user
from flask_login import current_user
from flask import g

from .userIdentification import randomIdentification
from .import_data_from_excel import read_data_from_excel, data_allocation_over_time_chart, data_performance_since_inception_chart


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

@app.route('/times_display')
@login_required
def times():
    return render_template('times_display.html', title="Times")


@app.route('/times_charts', methods=['GET', 'POST'])
@login_required
def times_charts():
    form = ExportDataForm()
    times_data = read_data_from_excel()

    positions_us_equities, positions_eu_equities, positions_jp_equities, positions_hk_equities, positions_us_bonds, \
    positions_uk_bonds, positions_eu_bonds, positions_ca_bonds, positions_jpy, positions_eur, positions_aud, \
    positions_cad, positions_gbp = data_allocation_over_time_chart(times_data)

    performance_total, performance_dates = data_performance_since_inception_chart(times_data)

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
                           performance_dates=performance_dates
                           )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


