# Contains view functions for various URLs
from app import app
from flask import render_template, json
from app.forms import LoginForm

# The home page of the application
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'AJ89720'}
    return render_template('index.html', title='Home', user=user)


# A Login form for users
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('form.html', title='Sign In', main_heading= 'Sign in', form=form)

# A Change Password form for users
@app.route('/changePass')
def changePass():
    form = ChangePassword()
    return render_template('form.html', title='Sign In', main_heading= 'Password Reset', form=form)


@app.route('/mainPage')
def mainPage():
    user = {'username': 'JS89652'}
    tableData = {'headers' : ['chrome', 'Safari', 'Mozilla', 'Firefox', 'NewCase'],
                 'rows' : [[0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0]]}
    lenHead = len(tableData['headers'])
    lenRow = len(tableData['rows'])
    return render_template('table.html', title='Home', user=user, tableData=tableData,lenHead=lenHead,lenRow=lenRow)

# An Output page containing charts
@app.route('/charts', methods=["GET"])
def createlchart():
    user = {'username': 'JS89652'}
    data = json.dumps([1.0, 2.0, 3.0])
    labels = json.dumps(["12-31-18", "01-01-19", "01-02-19"])
    return render_template('lineChart.html', title='Charts ', user=user, data=data, labels=labels)

@app.route('/mainPage2')
def mainPage2():
    user = {'username': 'JS89652'}
    tiles = [
        {
            'heading': 'Home',
            'img': 'Homebtn.png!'
        },
        {
            'heading': 'Login',
            'img': 'Homebtn.png'
        },
        {
            'heading': 'Analytics',
            'img': 'Homebtn.png'
        },
        {
            'heading': 'Help with Development',
            'img': 'Homebtn.png'
        }
    ]

    return render_template('Main2.html', title='Home', tiles=tiles)