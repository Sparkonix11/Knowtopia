from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Course, Material
import os
from werkzeug.utils import secure_filename

course_api_bp = Blueprint('course_api', __name__)

@course_api_bp.route('/courses', methods=['GET'])
def get_courses():
    try:
        courses = Course.query.all()
        course_data = []
        for course in courses:
            course_data.append({
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'image': course.image
            })
        return jsonify({'courses': course_data}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get courses: {str(e)}'}), 500
    
@course_api_bp.route('/instructor_courses', methods=['GET'])
@login_required
def get_instructor_courses():
    try:
        if not current_user.is_instructor:
            return jsonify({'error': 'User is not an instructor'}), 403
        
        courses = Course.query.filter_by(creator_user_id=current_user.id).all()
        course_data = []
        for course in courses:
            total_course_duration = 0
            weeks_data = []

            for week in course.weeks:
                total_week_duration = 0
                materials_data = []

                # Fetch all materials for the week
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
                    "week_id": week.user_id,
                    "week_name": week.name,
                    "materials": materials_data
                })

            course_data.append({
                "course_id": course.id,
                "course_name": course.name,
                "total_duration": total_course_duration,
                "weeks": weeks_data
            })
        return jsonify({'courses': course_data}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get courses: {str(e)}'}), 500
    
@course_api_bp.route('/course/<int:course_id>', methods=['GET'])
@login_required
def get_course(course_id):
    try:
        courses = Course.query.all()

        course_data = []

        for course in courses:
            total_course_duration = 0
            weeks_data = []

            for week in course.weeks:
                total_week_duration = 0
                materials_data = []

                # Fetch all materials for the week
                materials = Material.query.filter_by(week_id=week.id).all()

                for material in materials:
                    materials_data.append({
                        "material_id": material.user_id,
                        "material_name": material.name,
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
                "weeks": weeks_data
            })

        return jsonify({"courses": course_data}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch courses: {str(e)}"}), 500
    
@course_api_bp.route('/create_course', methods=['POST'])
@login_required
def create_course():
    try:
        if not current_user.is_instructor:
            return jsonify({'error': 'User is not an instructor'}), 403
        
        data = request.form
        required_fields = ['name', 'description']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        existing_course = Course.query.filter_by(name=data['name']).first()
        if existing_course:
            return jsonify({'error': 'Course already exists'}), 400
        
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

        return jsonify({'message': 'Course created', 'course': course_data}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create course: {str(e)}'}), 500
    
@course_api_bp.route('/delete_course/<int:course_id>', methods=['DELETE'])
@login_required
def delete_course(course_id):
    try:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        if course.creator_user_id != current_user.id:
            return jsonify({'error': 'User is not the creator of the course'}), 403
        
        db.session.delete(course)
        db.session.commit()
        
        return jsonify({'message': 'Course deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete course: {str(e)}'}), 500