from flask import Flask #import flask

# from app import create_app

app = Flask(__name__)   #create an app instance
# app = create_app()


from app import app


if __name__ == '__main__':
    app.run(debug=True)
