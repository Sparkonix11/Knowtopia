from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile('config.py')

    login_manager.init_app(app)
    return app