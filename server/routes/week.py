from flask import Blueprint, request, jsonify
from models import db, Week, Course
from flask_login import login_required, current_user

week_api_bp = Blueprint('week_api', __name__)

@week_api_bp.route('/create_week/<int:course_id>', methods=['POST'])
@login_required
def create_week(course_id):
    try:
        if not current_user.is_instructor:
            return jsonify({'error': 'User is not an instructor'}), 403
        data = request.form
        required_fields = ['name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        course = Course.query.filter_by(id=course_id).first()
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        if not course.creator_user_id == current_user.id:
            return jsonify({'error': 'User is not the creator of the course'}), 403
        
        existing_week = Week.query.filter_by(name=data['name'], course_id=course_id).first()
        if existing_week:
            return jsonify({'error': 'Week already exists'}), 400
        
        new_week = Week(
            name=data['name'],
            course_id=course_id
        )

        db.session.add(new_week)
        db.session.commit()

        week_data = {
            'id': new_week.id,
            'name': new_week.name,
        }

        return jsonify({'message': 'Week created', 'week': week_data}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create week: {str(e)}'}), 500
    
@week_api_bp.route('/delete_week/<int:week_id>', methods=['DELETE'])
@login_required
def delete_week(week_id):
    try:
        week = Week.query.get(week_id)
        if not week:
            return jsonify({'error': 'Week not found'}), 404
        
        course = Course.query.get(week.course_id)
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        if course.creator_user_id != current_user.id:
            return jsonify({'error': 'User is not the creator of the course'}), 403
        
        db.session.delete(week)
        db.session.commit()
        return jsonify({'message': 'Week deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete week: {str(e)}'}), 500