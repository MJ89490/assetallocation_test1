from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
# from assetallocation_UI import User

from flask_cors import CORS
from assetallocation_UI.aa_web_app.times_strategy.routes import times_strategy_bp

#todo create a function later

# CURRENT_PATH = os.path.dirname(__file__)

# todo create class there for effect_data (line 39) and then import class in routes_old.py
# slow down app at launch


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
app.register_blueprint(times_strategy_bp, url_prefix='/aa_web_app/times_strategy')
# app = Flask(__name__)
# app.wsgi_app = ReverseProxied(app.wsgi_app)
# app.debug = True
# CORS(app)

app.wsgi_app = ReverseProxied(app.wsgi_app)
app.debug = True
CORS(app)

bootstrap = Bootstrap(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'secret*'


# @login_manager.user_loader
# def load_user(user_id):
#     return User(user_id)
