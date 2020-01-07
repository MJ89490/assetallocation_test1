from flask import Flask #import flask


app = Flask(__name__)   #create an app instance

from app import app


if __name__ == '__main__':
    app.run(debug=True)
