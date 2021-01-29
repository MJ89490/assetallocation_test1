from flask import render_template, Flask
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route('/')
def home():
    return render_template('home_old.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)