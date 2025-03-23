from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, Assignment, Question, Score

class AssignmentSubmissionResource(Resource):
    @login_required
    def post(self, assignment_id):
        try:
            # Check if assignment exists
            assignment = Assignment.query.get(assignment_id)
            if not assignment:
                return {'error': 'Assignment not found'}, 404
            
            # Get the submitted answers from the request
            data = request.get_json()
            if not data or 'answers' not in data:
                return {'error': 'No answers provided'}, 400
            
            submitted_answers = data['answers']
            
            # Get all questions for this assignment
            questions = Question.query.filter_by(assignment_id=assignment_id).all()
            if not questions:
                return {'error': 'No questions found for this assignment'}, 404
            
            # Check if the student has already submitted this assignment
            existing_submission = Score.query.filter_by(
                student_id=current_user.id,
                assignment_id=assignment_id
            ).first()
            
            if existing_submission:
                return {'error': 'You have already submitted this assignment'}, 400
            
            # Evaluate the answers
            correct_count = 0
            total_questions = len(questions)
            
            for question in questions:
                question_id = str(question.id)
                if question_id in submitted_answers:
                    # For MCQ, check if the selected option matches the correct option
                    if submitted_answers[question_id] == question.correct_option:
                        correct_count += 1
            
            # Calculate score as a percentage
            score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
            
            # Create a new score record
            new_score = Score(
                student_id=current_user.id,
                assignment_id=assignment_id,
                score=correct_count,
                max_score=total_questions
            )
            
            db.session.add(new_score)
            db.session.commit()
            
            return {
                'message': 'Assignment submitted successfully',
                'score': {
                    'correct': correct_count,
                    'total': total_questions,
                    'percentage': score_percentage
                }
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to submit assignment: {str(e)}'}, 500

class AssignmentScoreResource(Resource):
    @login_required
    def get(self, assignment_id):
        try:
            # Check if assignment exists
            assignment = Assignment.query.get(assignment_id)
            if not assignment:
                return {'error': 'Assignment not found'}, 404
            
            # Get the score for this student and assignment
            score = Score.query.filter_by(
                student_id=current_user.id,
                assignment_id=assignment_id
            ).first()
            
            if not score:
                return {'message': 'You have not submitted this assignment yet'}, 404
            
            return {
                'score': {
                    'correct': score.score,
                    'total': score.max_score,
                    'percentage': (score.score / score.max_score) * 100 if score.max_score > 0 else 0,
                    'submitted_at': score.submitted_at.isoformat()
                }
            }, 200
            
        except Exception as e:
            return {'error': f'Failed to retrieve score: {str(e)}'}, 500