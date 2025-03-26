from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, Assignment, Score, Week, Course, Material
from sqlalchemy import func

class AssignmentScoresResource(Resource):
    @login_required
    def get(self, assignment_id):
        try:
            # Check if user is an instructor
            if not current_user.is_instructor:
                return {'error': 'Access denied. Only instructors can view all scores'}, 403
            
            # Check if assignment exists
            assignment = Assignment.query.get(assignment_id)
            if not assignment:
                return {'error': 'Assignment not found'}, 404
            
            # Get all scores for this assignment
            scores = Score.query.filter_by(assignment_id=assignment_id).all()
            
            if not scores:
                return {'message': 'No submissions for this assignment yet', 'scores': []}, 200
            
            # Format scores data
            scores_data = []
            for score in scores:
                percentage = (score.score / score.max_score) * 100 if score.max_score > 0 else 0
                scores_data.append({
                    'student_id': score.student_id,
                    'student_name': score.student.name if hasattr(score.student, 'name') else 'Unknown',
                    'score': score.score,
                    'max_score': score.max_score,
                    'percentage': percentage,
                    'submitted_at': score.submitted_at.isoformat()
                })
            
            # Calculate average percentage
            total_percentage = sum(score['percentage'] for score in scores_data)
            average_percentage = total_percentage / len(scores_data) if scores_data else 0
            
            # Get week and course information
            week = Week.query.get(assignment.week_id)
            course = Course.query.get(week.course_id) if week else None
            
            return {
                'assignment': {
                    'id': assignment.id,
                    'name': assignment.name,
                    'week_id': assignment.week_id,
                    'week_name': week.name if week else 'Unknown',
                    'course_id': course.id if course else None,
                    'course_name': course.name if course else 'Unknown'
                },
                'scores': scores_data,
                'average_percentage': average_percentage,
                'total_submissions': len(scores_data)
            }, 200
            
        except Exception as e:
            return {'error': f'Failed to retrieve scores: {str(e)}'}, 500

class AllAssignmentScoresResource(Resource):
    @login_required
    def get(self):
        try:
            # Check if user is an instructor
            if not current_user.is_instructor:
                return {'error': 'Access denied. Only instructors can view all scores'}, 403
            
            # Get all assignments for courses taught by this instructor
            # First, get all courses taught by this instructor
            courses = Course.query.filter_by(creator_user_id=current_user.id).all()
            
            if not courses:
                return {'message': 'No courses found for this instructor', 'assignments': []}, 200
            
            course_ids = [course.id for course in courses]
            
            # Get all weeks for these courses
            weeks = Week.query.filter(Week.course_id.in_(course_ids)).all()
            week_ids = [week.id for week in weeks]
            
            # Get all assignments for these weeks
            assignments = Assignment.query.filter(Assignment.week_id.in_(week_ids)).all()
            
            if not assignments:
                return {'message': 'No assignments found for your courses', 'assignments': []}, 200
            
            # For each assignment, get average score
            assignments_data = []
            for assignment in assignments:
                # Get all scores for this assignment
                scores = Score.query.filter_by(assignment_id=assignment.id).all()
                
                # Calculate average percentage if there are scores
                if scores:
                    total_percentage = sum((score.score / score.max_score) * 100 if score.max_score > 0 else 0 for score in scores)
                    average_percentage = total_percentage / len(scores)
                    submission_count = len(scores)
                else:
                    average_percentage = 0
                    submission_count = 0
                
                # Get week and course information
                week = Week.query.get(assignment.week_id)
                course = Course.query.get(week.course_id) if week else None
                
                assignments_data.append({
                    'id': assignment.id,
                    'name': assignment.name,
                    'week_id': assignment.week_id,
                    'week_name': week.name if week else 'Unknown',
                    'course_id': course.id if course else None,
                    'course_name': course.name if course else 'Unknown',
                    'average_percentage': average_percentage,
                    'submission_count': submission_count
                })
            
            return {'assignments': assignments_data}, 200
            
        except Exception as e:
            return {'error': f'Failed to retrieve assignment scores: {str(e)}'}, 500

# MaterialDoubtsResource has been moved to material_doubts.py

# AllMaterialDoubtsResource has been moved to material_doubts.py