
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from app import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
CSRFProtect(app).init_app(app)
bootstrap = Bootstrap(app)

# Import is at the bottom to avoid circular imports
from app import routes