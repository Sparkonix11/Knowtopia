from models import db
from sqlalchemy.sql import func

class EnrollmentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=func.now())
    
    student = db.relationship("User", backref="enrollment_requests")
    course = db.relationship("Course", backref="enrollment_requests")