from models import db
from sqlalchemy.sql import func

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())  
    week_id = db.Column(db.Integer, db.ForeignKey("week.id"), nullable=False)
    questions = db.relationship("Question", backref="question", cascade="all, delete-orphan")
