from models import db
from sqlalchemy.sql import func

class MaterialDoubt(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doubt_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    
    # Relationships
    material = db.relationship("Material", backref="doubts")
    student = db.relationship("User", backref="material_doubts")