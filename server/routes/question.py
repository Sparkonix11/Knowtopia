from flask import jsonify
from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from models import db, Question, Assignment

class QuestionCreateResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("question_description", required=True, help="Question description is required")
    parser.add_argument("option1", required=True, help="Option 1 is required")
    parser.add_argument("option2", required=True, help="Option 2 is required")
    parser.add_argument("option3", required=True, help="Option 3 is required")
    parser.add_argument("option4", required=True, help="Option 4 is required")
    parser.add_argument("correct_option", required=True, help="Correct option is required")

    @login_required
    def post(self, assignment_id):
        try:
            if not current_user.is_instructor:
                return {"error": "Access denied. Only instructors can add questions."}, 403

            assignment = Assignment.query.get(assignment_id)
            if not assignment:
                return {"error": "Invalid assignment_id"}, 404

            args = self.parser.parse_args()
            if args["correct_option"] not in ["1", "2", "3", "4"]:
                return {"error": "Correct option must be between 1 and 4"}, 400

            new_question = Question(
                description=args["question_description"],
                option1=args["option1"],
                option2=args["option2"],
                option3=args["option3"],
                option4=args["option4"],
                correct_option=args["correct_option"],
                assignment_id=assignment_id
            )
            db.session.add(new_question)
            db.session.commit()

            return {"message": "Question created", "question": {
                "id": new_question.id,
                "question_description": new_question.description,
                "option1": new_question.option1,
                "option2": new_question.option2,
                "option3": new_question.option3,
                "option4": new_question.option4,
                "correct_option": new_question.correct_option,
                "assignment_id": new_question.assignment_id
            }}, 201

        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to create question: {str(e)}"}, 500


class QuestionListResource(Resource):
    @login_required
    def get(self, assignment_id):
        try:
            assignment = Assignment.query.get(assignment_id)
            if not assignment:
                return {"error": "Invalid assignment_id"}, 404

            questions = Question.query.filter_by(assignment_id=assignment_id).all()
            questions_list = [{
                "id": q.id,
                "question_description": q.description,
                "option1": q.option1,
                "option2": q.option2,
                "option3": q.option3,
                "option4": q.option4,
                "correct_option": q.correct_option,
            } for q in questions]

            return {"questions": questions_list}, 200
        
        except Exception as e:
            return {"error": f"Failed to get questions: {str(e)}"}, 500


class QuestionDeleteResource(Resource):
    @login_required
    def delete(self, question_id):
        try:
            if not current_user.is_instructor:
                return {"error": "Access denied. Only instructors can delete questions."}, 403

            question = Question.query.get(question_id)
            if not question:
                return {"error": "Invalid question_id"}, 404

            db.session.delete(question)
            db.session.commit()
            return {"message": "Question deleted"}, 200
        
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to delete question: {str(e)}"}, 500
