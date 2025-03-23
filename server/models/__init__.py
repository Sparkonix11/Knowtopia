from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .assignment import Assignment
from .question import Question
from .review import Review
from .material import Material
from .week import Week
from .course import Course
from .enrollment import Enrollment
from.score import Score

def init_db(app):
    # Flask-Migrate will handle database creation and migrations
    # This function is kept for backward compatibility
    pass