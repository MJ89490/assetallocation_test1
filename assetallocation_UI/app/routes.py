# Contains view functions for various URLs
from flask import render_template
from flask import flash
from flask import url_for
from flask import redirect
from flask_login import logout_user
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/home')
def home():
    content = {'description': 'We need to add a short description regarding the front-end page'}
    return render_template('home.html', title='HomePage', content=content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("-------------------")
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print("******")
        print(username)
        print(password)
    return render_template('login.html', title='LoginPage', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

