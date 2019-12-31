from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from app import config

import jinja2
import os

CURRENT_PATH = os.path.dirname(__file__)

# Set the origin template (templates) of Flask and add subfolders
origin_path = "templates"
modals_path = os.path.abspath(os.path.join(CURRENT_PATH, "templates\modals"))
app = Flask(__name__)
template_folders = [origin_path, modals_path]

# Change the original folder of Flask by adding subfolders
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(template_folders),
])
app.config.from_object(config.DevelopmentConfig)
CSRFProtect(app).init_app(app)
bootstrap = Bootstrap(app)

# Import is at the bottom to avoid circular imports
from app import routes