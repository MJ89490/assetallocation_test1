# from flask import Flask
#
# app = Flask(__name__)
#
# from app import app
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


from app import app
from app import routes

if __name__ == '__main__':
    app.run(debug=True)






