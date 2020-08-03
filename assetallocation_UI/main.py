# from flask import Flask
#
# app = Flask(__name__)
#
# from app import app
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import app
from aa_web_app import routes

if __name__ == '__main__':
    app.run(debug=True)






