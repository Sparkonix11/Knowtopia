from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, Assignment, Week


class AssignmentResource(Resource):
    @login_required
    def get(self, assignment_id):
        try:
            assignment = Assignment.query.get(assignment_id)
            if not assignment:
                return {'error': 'Assignment not found'}, 404
            
            assignment_data = {
                'id': assignment.id,
                'name': assignment.name,
                'description': assignment.description,
                'week_id': assignment.week_id
            }
            return {'assignment': assignment_data}, 200
        except Exception as e:
            return {'error': f'Failed to retrieve assignment: {str(e)}'}, 500

class CreateAssignmentResource(Resource):
    @login_required
    def post(self, week_id):
        try:
            if not current_user.is_instructor:
                return {'error': 'Access denied. Only instructors can create assignments'}, 403
            
            week = Week.query.get(week_id)
            if not week:
                return {'error': 'Week not found'}, 404
            
            data = request.form
            required_fields = ['name', 'description']
            if not all(field in data for field in required_fields):
                return {'error': 'Missing required fields'}, 400
            
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
            return {'message': 'Assignment created', 'assignment': assignment_data}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create assignment: {str(e)}'}, 500

class DeleteAssignmentResource(Resource):
    @login_required
    def delete(self, assignment_id):
        try:
            if not current_user.is_instructor:
                return {'error': 'Access denied. Only instructors can delete assignments'}, 403
            
            assignment = Assignment.query.get(assignment_id)
            if not assignment:
                return {'error': 'Assignment not found'}, 404
            
            db.session.delete(assignment)
            db.session.commit()
            return {'message': 'Assignment deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete assignment: {str(e)}'}, 500