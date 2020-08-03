from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from assetallocation_UI.aa_web_app import config
from flask_login import LoginManager
from .models import User

from flask_cors import CORS
import jinja2
import os

#todo create a function later

CURRENT_PATH = os.path.dirname(__file__)


class ReverseProxied:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        return self.app(environ, start_response)


app = Flask(__name__, static_folder='static', static_url_path='/static')

app.wsgi_app = ReverseProxied(app.wsgi_app)
app.debug = True
CORS(app)

# Set the origin template (templates) of Flask and add subfolders
origin_path = "templates"
modals_icons_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\modalsIcons"))
modals_models_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\modalsModels"))
inputs_models_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\inputs_models"))
javascript_charts_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\js"))

template_folders = [origin_path, modals_icons_path, modals_models_path, inputs_models_path, javascript_charts_path]


# Change the original folder of Flask by adding subfolders
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(template_folders),
])

app.config.from_object(config.DevelopmentConfig)
CSRFProtect(app).init_app(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'secret*'


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)







# Set the origin template (templates) of Flask and add subfolders
# origin_path = "templates"
# modals_icons_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\modalsIcons"))
# modals_models_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\modalsModels"))
# inputs_models_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\inputs_models"))
# javascript_charts_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\js"))

# app_old = Flask(__name__)

# template_folders = [origin_path, modals_icons_path, modals_models_path, inputs_models_path, javascript_charts_path]


# # Change the original folder of Flask by adding subfolders
# app_old.jinja_loader = jinja2.ChoiceLoader([
#     app_old.jinja_loader,
#     jinja2.FileSystemLoader(template_folders),
# ])
#
# app_old.config.from_object(config.DevelopmentConfig)
# CSRFProtect(app_old).init_app(app_old)
# bootstrap = Bootstrap(app_old)
#
# login_manager = LoginManager()
# login_manager.init_app(app_old)
# login_manager.login_view = 'login'
# app_old.config['SECRET_KEY'] = 'secret*'


# @login_manager.user_loader
# def load_user(user_id):
#     return User(user_id)