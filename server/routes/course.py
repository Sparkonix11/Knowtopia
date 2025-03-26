from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, Course, Material, Enrollment, User
import os
from werkzeug.utils import secure_filename

THUMBNAIL_FOLDER = "uploads/thumbnails"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

class CourseResource(Resource):
    def get(self):
        try:
            courses = Course.query.all()
            course_data = []
            for course in courses:
                course_data.append({
                    'id': course.id,
                    'name': course.name,
                    'description': course.description,
                    'thumbnail_path': course.thumbnail_path
                })
            return {'courses': course_data}, 200
        except Exception as e:
            return {'error': f'Failed to get courses: {str(e)}'}, 500

class SingleCourseResource(Resource):
    @login_required
    def get(self, course_id):
        try:
            # Get the course by ID
            course = Course.query.get(course_id)
            if not course:
                return {'error': 'Course not found'}, 404
            
            # Check if user has access to this course
            if current_user.is_instructor:
                # For instructors, check if they created the course
                if course.creator_user_id != current_user.id:
                    return {'error': 'You do not have access to this course'}, 403
            else:
                # For students, check if they are enrolled
                enrollment = Enrollment.query.filter_by(
                    student_id=current_user.id, 
                    course_id=course_id
                ).first()
                if not enrollment:
                    return {'error': 'You are not enrolled in this course'}, 403
            
            # Calculate total course duration and prepare weeks data
            total_course_duration = 0
            weeks_data = []
            
            for week in course.weeks:
                total_week_duration = 0
                materials_data = []
                materials = Material.query.filter_by(week_id=week.id).all()
                
                for material in materials:
                    total_week_duration += material.duration
                    materials_data.append({
                        "material_id": material.id,
                        "material_name": material.name,
                        "duration": material.duration,
                        "file_path": material.file_path,
                        "type": "video"  # Default type, can be updated based on actual data
                    })
                
                # Get assignments for this week
                from models import Assignment
                assignments = Assignment.query.filter_by(week_id=week.id).all()
                for assignment in assignments:
                    materials_data.append({
                        "material_id": assignment.id,
                        "material_name": assignment.name,
                        "description": assignment.description,
                        "isAssignment": True,
                        "assignment_id": assignment.id,
                        "type": "assignment",
                        "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                        "questions": [{
                            "id": question.id,
                            "description": question.description,
                            "options": [question.option1, question.option2, question.option3, question.option4],
                            "correct_answer": question.correct_option
                        } for question in assignment.questions]
                    })
                
                total_course_duration += total_week_duration
                weeks_data.append({
                    "id": week.id,
                    "name": week.name,
                    "materials": materials_data
                })
            
            # Prepare the course data with weeks and materials
            course_data = {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "thumbnail_path": course.thumbnail_path,
                "duration": total_course_duration,
                "weeks": weeks_data
            }
            
            return {'course': course_data}, 200
        except Exception as e:
            return {'error': f'Failed to get course: {str(e)}'}, 500

class InstructorCoursesResource(Resource):
    @login_required
    def get(self):
        try:
            if not current_user.is_instructor:
                return {'error': 'User is not an instructor'}, 403
            
            courses = Course.query.filter_by(creator_user_id=current_user.id).all()
            course_data = []

            for course in courses:
                total_course_duration = 0
                weeks_data = []

                for week in course.weeks:
                    total_week_duration = 0
                    materials_data = []
                    materials = Material.query.filter_by(week_id=week.id).all()

                    for material in materials:
                        total_week_duration += material.duration
                        materials_data.append({
                            "material_id": material.id,
                            "material_name": material.name,
                            "duration": material.duration,
                            "file_path": material.filename
                        })
                    
                    # Get assignments for this week
                    # from models import Assignment
                    # assignments = Assignment.query.filter_by(week_id=week.id).all()
                    # for assignment in assignments:
                    #     materials_data.append({
                    #         "material_id": assignment.id,
                    #         "material_name": assignment.name,
                    #         "description": assignment.description,
                    #         "isAssignment": True,
                    #         "assignment_id": assignment.id,
                    #         "type": "assignment",
                    #         "questions": [{
                    #             "id": question.id,
                    #             "text": question.description,
                    #             "options": question.options,
                    #             "correct_answer": question.correct_answer
                    #         } for question in assignment.questions]
                    #     })
                    
                    total_course_duration += total_week_duration
                    weeks_data.append({
                        "id": week.id,
                        "name": week.name,
                        "materials": materials_data
                    })
                
                course_data.append({
                    "id": course.id,
                    "name": course.name,
                    "description": course.description,
                    "thumbnail_path": course.thumbnail_path,
                    "duration": total_course_duration,
                    "weeks": weeks_data
                })
            
            return {'courses': course_data}, 200
        except Exception as e:
            return {'error': f'Failed to get courses: {str(e)}'}, 500

class CreateCourseResource(Resource):
    @login_required
    def post(self):
        try:
            if not current_user.is_instructor:
                return {'error': 'User is not an instructor'}, 403
            
            data = request.form
            required_fields = ['name', 'description']
            if not all(field in data for field in required_fields):
                return {'error': 'Missing required fields'}, 400
            
            existing_course = Course.query.filter_by(name=data['name']).first()
            if existing_course:
                return {'error': 'Course already exists'}, 400
            
            new_course = Course(
                name=data['name'],
                description=data['description'],
                creator_user_id=current_user.id
            )
            
            db.session.add(new_course)
            db.session.flush()
            
            file = request.files.get('thumbnail')
            if file:
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit(".", 1)[-1].lower()
                if file_ext not in ALLOWED_EXTENSIONS:
                    return {'error': 'File type not allowed'}, 400
                
                if not os.path.exists(THUMBNAIL_FOLDER):
                    os.makedirs(THUMBNAIL_FOLDER)
                
                image_filename = secure_filename(f"{new_course.id}.{file_ext}")
                image_path = os.path.join(THUMBNAIL_FOLDER, image_filename)
                file.save(image_path)
                new_course.thumbnail_path = f"/{THUMBNAIL_FOLDER}/{image_filename}"


                # filename = secure_filename(file.filename)
                # thumbnail_path = os.path.join('uploads/materials', filename)
                # os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
                # file.save(thumbnail_path)
                        
            db.session.commit()
            
            course_data = {
                'id': new_course.id,
                'name': new_course.name,
                'description': new_course.description,
                'thumbnail_path': new_course.thumbnail_path
            }
            
            return {'message': 'Course created', 'course': course_data}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create course: {str(e)}'}, 500

class DeleteCourseResource(Resource):
    @login_required
    def delete(self, course_id):
        try:
            if not current_user.is_instructor:
                return {'error': 'User is not an instructor'}, 403
            course = Course.query.get(course_id)
            if not course:
                return {'error': 'Course not found'}, 404
            
            if course.creator_user_id != current_user.id:
                return {'error': 'User is not the creator of the course'}, 403
            
            db.session.delete(course)
            db.session.commit()
            return {'message': 'Course deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete course: {str(e)}'}, 500
        
class EnrolledCoursesResource(Resource):
    @login_required
    def get(self):
        try:
            enrolled_courses = Course.query.join(Enrollment).filter(Enrollment.student_id == current_user.id).all()
            
            course_data = []
            for course in enrolled_courses:
                course_data.append({
                    'id': course.id,
                    'name': course.name,
                    'description': course.description,
                    'thumbnail_path': course.thumbnail_path
                })
            
            return {'enrolled_courses': course_data}, 200
        except Exception as e:
            return {'error': f'Failed to get enrolled courses: {str(e)}'}, 500
        
class EnrollStudentResource(Resource):
    @login_required
    def post(self, course_id, student_id):
        try:
            if not current_user.is_instructor:
                return {'error': 'Only instructors can enroll students'}, 403

            course = Course.query.get(course_id)
            if not course:
                return {'error': 'Course not found'}, 404

            if course.creator_user_id != current_user.id:
                return {'error': 'You can only enroll students in your own course'}, 403

            student = User.query.get(student_id)
            if not student or student.is_instructor:
                return {'error': 'Invalid student ID'}, 400

            existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
            if existing_enrollment:
                return {'error': 'Student is already enrolled in this course'}, 400

            enrollment = Enrollment(student_id=student_id, course_id=course_id)
            db.session.add(enrollment)
            db.session.commit()

            return {'message': 'Student enrolled successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to enroll student: {str(e)}'}, 500

