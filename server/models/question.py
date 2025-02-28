from models import db
from sqlalchemy.sql import func

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)  
    created_at = db.Column(db.DateTime, default=func.now()) 
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"), nullable=False)