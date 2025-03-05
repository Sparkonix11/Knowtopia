from flask import Blueprint, request, jsonify
from models import db, Question, Assignment
from flask_login import login_required, current_user

question_api_bp = Blueprint('question_api', __name__)

@question_api_bp.route("/<int:assignment_id>/create", methods=["POST"])
@login_required
def create_question(assignment_id):
    try:
        if not current_user.is_instructor:
            return jsonify({"error": "Access denied. Only instructors can add questions."}), 403

        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"error": "Invalid assignment_id"}), 404

        data = request.form
        required_fields = ["question_description", "option1", "option2", "option3", "option4", "correct_option"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        if data["correct_option"] not in ["1", "2", "3", "4"]:
            return jsonify({"error": "Correct option must be between 1 and 4"}), 400
        
        new_question = Question(
            description=data["question_description"],
            option1=data["option1"],
            option2=data["option2"],
            option3=data["option3"],
            option4=data["option4"],
            correct_option=data["correct_option"],
            assignment_id=assignment_id
        )
        new_question_data = {
            "question_description": new_question.description,
            "option1": new_question.option1,
            "option2": new_question.option2,
            "option3": new_question.option3,
            "option4": new_question.option4,
            "correct_option": new_question.correct_option,
            "assignment_id": new_question.assignment_id
        }
        
        db.session.add(new_question)
        db.session.commit()

        return jsonify({"message": "Question created", "question": new_question_data}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create question: {str(e)}'}), 500
    
@question_api_bp.route("/<int:assignment_id>/questions/", methods=["GET"])
@login_required
def get_questions(assignment_id):
    try:
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"error": "Invalid assignment_id"}), 404

        questions = Question.query.filter_by(assignment_id=assignment_id).all()
        
        questions_list = []
        for question in questions:
            question_data = {
                "id": question.id,
                "question_description": question.description,
                "option1": question.option1,
                "option2": question.option2,
                "option3": question.option3,
                "option4": question.option4,
                "correct_option": question.correct_option,
            }
            questions_list.append(question_data)

        return jsonify({"questions": questions_list}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get questions: {str(e)}"}), 500
    
@question_api_bp.route("/<int:question_id>/delete", methods=["DELETE"])
@login_required
def delete_question(question_id):
    try:
        if not current_user.is_instructor:
            return jsonify({"error": "Access denied. Only instructors can delete questions."}), 403

        question = Question.query.get(question_id)
        if not question:
            return jsonify({"error": "Invalid question_id"}), 404

        db.session.delete(question)
        db.session.commit()
        return jsonify({"message": "Question deleted"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete question: {str(e)}"}), 500

