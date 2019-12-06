# Contains view functions for various URLs
from app import app
from app.forms import LoginForm
from flask import render_template #html templates
from flask import redirect
from flask import flash
from flask import url_for

@app.route('/')
@app.route('/home')
def home():
    user = {'username': 'AJ89720'}
    return render_template('home.html', title='HomePage', user=user)

# A Login form for users
@app.route('/login', methods=['GET', 'POST'])
#GET: returns the information to the client
#PUT: the browser submits form data to tge server
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #flash function: show a message to the user
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        #redirect function: client we browser automatically navigate to a different page ---> home page
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


# The home page of the application
# @app.route('/')
# @app.route('/index')
# def index():
#     user = {'username': 'AJ89720'}
#     return render_template('home.html', title='Home', user=user)



#
# # A Change Password form for users
# @app.route('/changePass')
# def changePass():
#     form = ChangePassword()
#     return render_template('form.html', title='Sign In', main_heading= 'Password Reset', form=form)


# @app.route('/mainPage')
# def mainPage():
#     user = {'username': 'JS89652'}
#     tableData = {'headers' : ['chrome', 'Safari', 'Mozilla', 'Firefox', 'NewCase'],
#                  'rows' : [[0, 0, 0, 0, 0],
#                            [1, 0, 0, 0, 0],
#                            [0, 1, 0, 0, 0],
#                            [0, 0, 1, 0, 0],
#                            [0, 0, 0, 1, 0]]}
#     lenHead = len(tableData['headers'])
#     lenRow = len(tableData['rows'])
#     return render_template('table.html', title='Home', user=user, tableData=tableData,lenHead=lenHead,lenRow=lenRow)
#
# # An Output page containing charts
# @app.route('/charts', methods=["GET"])
# def createlchart():
#     user = {'username': 'JS89652'}
#     data = json.dumps([1.0, 2.0, 3.0])
#     labels = json.dumps(["12-31-18", "01-01-19", "01-02-19"])
#     return render_template('lineChart.html', title='Charts ', user=user, data=data, labels=labels)
#
# @app.route('/mainPage2')
# def mainPage2():
#     user = {'username': 'JS89652'}
#     tiles = [
#         {
#             'heading': 'Home',
#             'img': 'Homebtn.png!'
#         },
#         {
#             'heading': 'Login',
#             'img': 'Homebtn.png'
#         },
#         {
#             'heading': 'Analytics',
#             'img': 'Homebtn.png'
#         },
#         {
#             'heading': 'Help with Development',
#             'img': 'Homebtn.png'
#         }
#     ]
#
#     return render_template('Main2.html', title='Home', tiles=tiles)
#
