from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, Course, Material, Enrollment, User
import os
from werkzeug.utils import secure_filename

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
                    
                    total_course_duration += total_week_duration
                    weeks_data.append({
                        "week_id": week.id,
                        "week_name": week.name,
                        "materials": materials_data
                    })
                
                course_data.append({
                    "course_id": course.id,
                    "course_name": course.name,
                    "total_duration": total_course_duration,
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
            
            file = request.files.get('thumbnail')
            thumbnail_path = None
            if file:
                filename = secure_filename(file.filename)
                thumbnail_path = os.path.join('uploads/materials', filename)
                os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
                file.save(thumbnail_path)
            
            new_course = Course(
                name=data['name'],
                description=data['description'],
                creator_user_id=current_user.id,
                thumbnail_path=thumbnail_path
            )
            
            db.session.add(new_course)
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

