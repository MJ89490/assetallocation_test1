# from flask import Flask
#
# app_old = Flask(__name__)
#
# from app_old import app_old
#
#
# if __name__ == '__main__':
#     app_old.run(debug=True)


from assetallocation_UI.aa_web_app import app
from assetallocation_UI.aa_web_app import routes

if __name__ == '__main__':
    app.run(debug=True)






