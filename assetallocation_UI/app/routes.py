# Contains view functions for various URLs
from flask import render_template
from flask import flash
from flask import url_for
from flask import redirect
from app import app
from app.forms import LoginForm, ExportDataForm
from .models import User

from flask_login import login_required
from flask_login import logout_user
from flask_login import login_user
from flask_login import current_user
from flask import g

from .userIdentification import randomIdentification

from .times_charts import chart_performance, bar_chart

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
    from flask import request

    if request.method == "POST":
        if request.form['submit_button'] == 'selectInputToExport':
            print(form.start_date.data)
            print(form.end_date.data)
        elif request.form['submit_button'] == 'selectInputOk':
            print(form.inputs.data)

    return render_template('new_dashboard_js.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


