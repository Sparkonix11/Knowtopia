from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from models.course import Course
from models.material import Material
from models.assignment import Assignment
from models.user import User
from models.week import Week
from flask_login import login_required, current_user

class SearchResource(Resource):
    @login_required
    def get(self):
        query = request.args.get('query', '')
        if not query or len(query) < 3:
            return {'message': 'Search query must be at least 3 characters long'}, 400
        
        # Get current user - using flask-login's current_user
        
        # Search results containers
        courses_results = []
        materials_results = []
        assignments_results = []
        
        # Search in courses
        if current_user.is_instructor:
            # Instructors can see their own courses
            courses = Course.query.filter(
                Course.instructor_id == current_user.id,
                or_(
                    Course.name.ilike(f'%{query}%'),
                    Course.description.ilike(f'%{query}%')
                )
            ).all()
        else:
            # Students can see enrolled courses
            courses = Course.query.join(Course.enrollments).filter(
                Course.enrollments.any(student_id=current_user.id),
                or_(
                    Course.name.ilike(f'%{query}%'),
                    Course.description.ilike(f'%{query}%')
                )
            ).all()
            
        for course in courses:
            courses_results.append({
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'type': 'course'
            })
        
        # Search in materials
        if current_user.is_instructor:
            # Instructors can see materials in their courses
            materials = Material.query.join(Week, Material.week_id == Week.id).join(Course).filter(
                Course.instructor_id == current_user.id,
                or_(
                    Material.name.ilike(f'%{query}%')
                )
            ).all()
        else:
            # Students can see materials in enrolled courses
            materials = Material.query.join(Week, Material.week_id == Week.id).join(Course).join(Course.enrollments).filter(
                Course.enrollments.any(student_id=current_user.id),
                or_(
                    Material.name.ilike(f'%{query}%')
                )
            ).all()
            
        for material in materials:
            # Get the week to access course_id
            week = Week.query.get(material.week_id)
            materials_results.append({
                'id': material.id,
                'title': material.name,  # Using name instead of title
                'description': '',  # Material doesn't have description field
                'course_id': week.course_id if week else None,
                'week_id': material.week_id,
                'type': 'material'
            })
        
        # Search in assignments
        if current_user.is_instructor:
            # Instructors can see assignments in their courses
            assignments = Assignment.query.join(Assignment.week).join(Course).filter(
                Course.instructor_id == current_user.id,
                or_(
                    Assignment.name.ilike(f'%{query}%'),
                    Assignment.description.ilike(f'%{query}%')
                )
            ).all()
        else:
            # Students can see assignments in enrolled courses
            assignments = Assignment.query.join(Assignment.week).join(Course).join(Course.enrollments).filter(
                Course.enrollments.any(student_id=current_user.id),
                or_(
                    Assignment.name.ilike(f'%{query}%'),
                    Assignment.description.ilike(f'%{query}%')
                )
            ).all()
            
        for assignment in assignments:
            assignments_results.append({
                'id': assignment.id,
                'title': assignment.name,  # Using name instead of title
                'description': assignment.description,
                'course_id': assignment.week.course_id,
                'week_id': assignment.week_id,
                'type': 'assignment'
            })
        
        # Combine all results
        all_results = courses_results + materials_results + assignments_results
        
        return {
            'results': all_results,
            'count': len(all_results)
        }, 200