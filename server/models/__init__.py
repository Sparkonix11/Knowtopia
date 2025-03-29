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
from .score import Score
from .material_doubt import MaterialDoubt
from .enrollment_request import EnrollmentRequest

def init_db(app):
    with app.app_context():
        db.create_all()