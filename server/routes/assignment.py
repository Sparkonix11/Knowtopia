from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Assignment, Week

assignment_api_bp = Blueprint('assignment_api', __name__)

@assignment_api_bp.route('/<int:week_id>/create', methods=['POST'])
@login_required
def create_assignment(week_id):
    try:
        if not current_user.is_instructor:
            return jsonify({'error': 'Access denied. Only instructors can create assignments'}), 403
        week = Week.query.get(week_id)
        if not week:
            return jsonify({'error': 'Week not found'}), 404
        
        data = request.form
        required_fields = ['name', 'description']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        new_assignment = Assignment(
            name=data['name'],
            description=data['description'],
            week_id=week_id
        )

        db.session.add(new_assignment)
        db.session.commit()

        assignment_data = {
            'id': new_assignment.id,
            'name': new_assignment.name,
            'description': new_assignment.description,
            'week_id': new_assignment.week_id
        }
        return jsonify({'message': 'Assignment created', 'assignment': assignment_data}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create assignment: {str(e)}'}), 500
    
@assignment_api_bp.route('<int:assignment_id>/delete', methods=['DELETE'])
@login_required
def delete_assignment(assignment_id):
    try:
        if not current_user.is_instructor:
            return jsonify({'error': 'Access denied. Only instructors can delete assignments'}), 403
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({'error': 'Assignment not found'}), 404
        db.session.delete(assignment)
        db.session.commit()
        return jsonify({'message': 'Assignment deleted'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete assignment: {str(e)}'}), 500
    
@assignment_api_bp.route('/<int:assignment_id>/', methods=['GET'])
@login_required
def get_assignment(assignment_id):
    try:
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({'error': 'Assignment not found'}), 404
        assignment_data = {
            'id': assignment.id,
            'name': assignment.name,
            'description': assignment.description,
            'week_id': assignment.week_id
        }
        return jsonify({'assignment': assignment_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve assignment: {str(e)}'}), 500