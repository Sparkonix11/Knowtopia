from flask import request, jsonify
from flask_restful import Resource
from models import db, Week, Course
from flask_login import login_required, current_user

class WeekCreateResource(Resource):
    @login_required
    def post(self, course_id):
        try:
            if not current_user.is_instructor:
                return {'error': 'User is not an instructor'}, 403

            data = request.form
            if 'name' not in data:
                return {'error': 'Missing required fields'}, 400

            course = Course.query.get(course_id)
            if not course:
                return {'error': 'Course not found'}, 404

            if course.creator_user_id != current_user.id:
                return {'error': 'User is not the creator of the course'}, 403

            if Week.query.filter_by(name=data['name'], course_id=course_id).first():
                return {'error': 'Week already exists'}, 400

            new_week = Week(
                name=data['name'],
                course_id=course_id,
                user_id=current_user.id
            )

            db.session.add(new_week)
            db.session.commit()

            return {'message': 'Week created', 'week': {
                'id': new_week.id,
                'name': new_week.name,
                'course_id': new_week.course_id,
                'user_id': new_week.user_id
            }}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create week: {str(e)}'}, 500

class WeekDeletionResource(Resource):
    @login_required
    def delete(self, course_id, week_id):
        try:
            week = Week.query.get(week_id)
            if not week:
                return {'error': 'Week not found'}, 404

            course = Course.query.get(course_id)
            if not course:
                return {'error': 'Course not found'}, 404

            if week.user_id != current_user.id:
                return {'error': 'User is not the creator of the course'}, 403

            db.session.delete(week)
            db.session.commit()
            return {'message': 'Week deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete week: {str(e)}'}, 500
