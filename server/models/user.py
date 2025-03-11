from models import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45))
    fname = db.Column(db.String(45))
    lname = db.Column(db.String(45))
    is_instructor = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(10), nullable=True)
    image = db.Column(db.String(100), default='/static/user_placeholder.png')

    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")

