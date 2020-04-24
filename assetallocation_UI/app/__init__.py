from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from app import config
from flask_login import LoginManager
from .models import User

import jinja2
import os


#todo create a function later

CURRENT_PATH = os.path.dirname(__file__)

# Set the origin template (templates) of Flask and add subfolders
origin_path = "templates"
modals_icons_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\modalsIcons"))
modals_models_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\modalsModels"))
inputs_models_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\inputs_models"))
javascript_charts_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\js"))

# Set the origin staic folder (static) of Flask and add subfolders
origin_path_static = "static"
css_style_path = os.path.abspath(os.path.join(CURRENT_PATH, "static\img"))
javascript_path = os.path.abspath(os.path.join(CURRENT_PATH, "static\js"))
app = Flask(__name__)

template_folders = [origin_path, modals_icons_path, modals_models_path, inputs_models_path, javascript_charts_path]
static_folders = [origin_path_static, css_style_path, javascript_path]

# Change the original folder of Flask by adding subfolders
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(template_folders),
])
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(static_folders),
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

# Import is at the bottom to avoid circular imports
from app import routes



# def create_app():
#     # Set the origin template (templates) of Flask and add subfolders
#     origin_path = "templates"
#     modals_icons_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\modalsIcons"))
#     modals_models_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\modalsModels"))
#     inputs_models_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\inputs_models"))
#
#     app = Flask(__name__, instance_relative_config=False)
#
#     template_folders = [origin_path, modals_icons_path, modals_models_path, inputs_models_path]
#     # Change the original folder of Flask by adding subfolders
#     app.jinja_loader = jinja2.ChoiceLoader([
#         app.jinja_loader,
#         jinja2.FileSystemLoader(template_folders),
#     ])
#
#     app.config.from_object(config.DevelopmentConfig)
#     CSRFProtect(app).init_app(app)
#     bootstrap = Bootstrap(app)
#
#     dash_app = dashview.A
#     login_manager = LoginManager()
#     login_manager.init_app(app)
#     login_manager.login_view = 'login'
#     app.config['SECRET_KEY'] = 'secret*'
#
#     @login_manager.user_loader
#     def load_user(user_id):
#         return User(user_id)
#
#     # Import is at the bottom to avoid circular imports
#     from app import routes