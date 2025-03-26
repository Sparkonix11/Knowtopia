from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, Assignment, Week
from datetime import datetime


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
                'due_date': assignment.due_date.isoformat() if assignment.due_date else None,
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
            
            # Parse due_date if provided
            due_date = None
            if 'due_date' in data and data['due_date']:
                try:
                    # Parse the date string from frontend
                    due_date = datetime.strptime(data['due_date'], '%Y-%m-%dT%H:%M')
                except ValueError:
                    return {'error': 'Invalid due date format'}, 400
            
            new_assignment = Assignment(
                name=data['name'],
                description=data['description'],
                due_date=due_date,
                week_id=week_id
            )
            db.session.add(new_assignment)
            db.session.commit()
            
            assignment_data = {
                'id': new_assignment.id,
                'name': new_assignment.name,
                'description': new_assignment.description,
                'due_date': new_assignment.due_date.isoformat() if new_assignment.due_date else None,
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