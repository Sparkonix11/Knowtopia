from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, EnrollmentRequest, Course, User, Enrollment

class EnrollmentRequestResource(Resource):
    @login_required
    def post(self):
        """Create a new enrollment request"""
        try:
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400
            
            course_id = data.get("course_id")
            message = data.get("message", "")
            
            if not course_id:
                return {"error": "Course ID is required"}, 400
            
            # Check if the course exists
            course = Course.query.get(course_id)
            if not course:
                return {"error": "Course not found"}, 404
            
            # Check if the user is already enrolled
            existing_enrollment = Enrollment.query.filter_by(
                student_id=current_user.id, 
                course_id=course_id
            ).first()
            if existing_enrollment:
                return {"error": "You are already enrolled in this course"}, 400
            
            # Check if there's already a pending request
            existing_request = EnrollmentRequest.query.filter_by(
                student_id=current_user.id,
                course_id=course_id,
                status="pending"
            ).first()
            if existing_request:
                return {"error": "You already have a pending enrollment request for this course"}, 400
            
            # Create the enrollment request
            enrollment_request = EnrollmentRequest(
                student_id=current_user.id,
                course_id=course_id,
                message=message
            )
            
            db.session.add(enrollment_request)
            db.session.commit()
            
            return {"message": "Enrollment request submitted successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to submit enrollment request: {str(e)}"}, 500

class StudentEnrollmentRequestsResource(Resource):
    @login_required
    def get(self):
        """Get all enrollment requests for the current student"""
        try:
            requests = EnrollmentRequest.query.filter_by(student_id=current_user.id).all()
            
            requests_data = []
            for req in requests:
                course = Course.query.get(req.course_id)
                requests_data.append({
                    "id": req.id,
                    "course_id": req.course_id,
                    "course_name": course.name if course else "Unknown",
                    "message": req.message,
                    "status": req.status,
                    "created_at": req.created_at.isoformat()
                })
            
            return {"enrollment_requests": requests_data}, 200
        except Exception as e:
            return {"error": f"Failed to get enrollment requests: {str(e)}"}, 500

class InstructorEnrollmentRequestsResource(Resource):
    @login_required
    def get(self):
        """Get all enrollment requests for courses created by the instructor"""
        try:
            if not current_user.is_instructor:
                return {"error": "Only instructors can access this resource"}, 403
            
            # Get all courses created by the instructor
            instructor_courses = Course.query.filter_by(creator_user_id=current_user.id).all()
            course_ids = [course.id for course in instructor_courses]
            
            # Get all enrollment requests for these courses
            requests = EnrollmentRequest.query.filter(EnrollmentRequest.course_id.in_(course_ids)).all()
            
            requests_data = []
            for req in requests:
                student = User.query.get(req.student_id)
                course = Course.query.get(req.course_id)
                
                requests_data.append({
                    "id": req.id,
                    "student_id": req.student_id,
                    "student_name": f"{student.fname} {student.lname}" if student else "Unknown",
                    "student_email": student.email if student else "Unknown",
                    "course_id": req.course_id,
                    "course_name": course.name if course else "Unknown",
                    "message": req.message,
                    "status": req.status,
                    "created_at": req.created_at.isoformat()
                })
            
            return {"enrollment_requests": requests_data}, 200
        except Exception as e:
            return {"error": f"Failed to get enrollment requests: {str(e)}"}, 500

class EnrollmentRequestActionResource(Resource):
    @login_required
    def post(self, request_id):
        """Approve or reject an enrollment request"""
        try:
            if not current_user.is_instructor:
                return {"error": "Only instructors can perform this action"}, 403
            
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400
            
            action = data.get("action")
            if action not in ["approve", "reject"]:
                return {"error": "Invalid action. Must be 'approve' or 'reject'"}, 400
            
            # Get the enrollment request
            enrollment_request = EnrollmentRequest.query.get(request_id)
            if not enrollment_request:
                return {"error": "Enrollment request not found"}, 404
            
            # Check if the instructor owns the course
            course = Course.query.get(enrollment_request.course_id)
            if not course or course.creator_user_id != current_user.id:
                return {"error": "You don't have permission to manage this enrollment request"}, 403
            
            if action == "approve":
                # Check if the student is already enrolled
                existing_enrollment = Enrollment.query.filter_by(
                    student_id=enrollment_request.student_id, 
                    course_id=enrollment_request.course_id
                ).first()
                
                if not existing_enrollment:
                    # Create a new enrollment
                    enrollment = Enrollment(
                        student_id=enrollment_request.student_id,
                        course_id=enrollment_request.course_id
                    )
                    db.session.add(enrollment)
                
                enrollment_request.status = "approved"
                message = "Enrollment request approved successfully"
            else:  # reject
                enrollment_request.status = "rejected"
                message = "Enrollment request rejected successfully"
            
            db.session.commit()
            return {"message": message}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to process enrollment request: {str(e)}"}, 500