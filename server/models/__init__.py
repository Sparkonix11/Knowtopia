from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User

def init_db(app):
    with app.app_context():
        db.create_all()