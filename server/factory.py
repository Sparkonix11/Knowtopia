from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from models import db, init_db, User
from routes import init_routes

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    init_db(app)
    login_manager.init_app(app)

    init_routes(app)
    return app