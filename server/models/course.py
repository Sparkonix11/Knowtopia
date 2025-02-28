from models import db
from sqlalchemy.sql import func

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    creator_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())  
    thumbnail_path = db.Column(db.String(255))  
    weeks = db.relationship("Week", backref="week",cascade="all,delete-orphan")  