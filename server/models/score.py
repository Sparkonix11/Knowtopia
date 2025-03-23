from models import db
from sqlalchemy.sql import func

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime, default=func.now())
    
    # Define relationships
    student = db.relationship("User", backref="scores")
    assignment = db.relationship("Assignment", backref="scores")