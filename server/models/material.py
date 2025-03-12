from models import db
from sqlalchemy.sql import func

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey("week.id"), nullable=False)
    duration = db.Column(db.Integer,nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255))
    transcript_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=func.now())  
    #course = db.relationship("Week", backref="materials")
    reviews = db.relationship("Review", backref="review", cascade="all, delete-orphan")