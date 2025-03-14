from tests import ENDPOINTS
from tests.conftest import create_test_question, delete_test_question, create_test_assignment, delete_test_assignment

def test_create_question(instructor_session):
    """Test instructor successfully creating a question"""
    course_id, week_id, assignment_id, question_id = create_test_question(instructor_session)
    delete_test_question(instructor_session, course_id, week_id, assignment_id, question_id)

def test_create_question_unauthorized(student_session, instructor_session):
    """Test student attempting to create a question (should be unauthorized)"""
    course_id, week_id, assignment_id = create_test_assignment(instructor_session)
    response = student_session.post(ENDPOINTS["question_create"].format(assignment_id=assignment_id), data={
        "question_description": "Sample question?",
        "option1": "A",
        "option2": "B",
        "option3": "C",
        "option4": "D",
        "correct_option": "1"
    })
    assert response.status_code == 403
    assert response.json()["error"] == "Access denied. Only instructors can add questions."
    delete_test_assignment(instructor_session, course_id, week_id, assignment_id)

def test_create_question_invalid_assignment(instructor_session):
    """Test creating a question with an invalid assignment_id"""
    response = instructor_session.post(ENDPOINTS["question_create"].format(assignment_id=9999), data={
        "question_description": "Invalid assignment question?",
        "option1": "A",
        "option2": "B",
        "option3": "C",
        "option4": "D",
        "correct_option": "1"
    })
    assert response.status_code == 404
    assert response.json()["error"] == "Invalid assignment_id"

def test_create_question_invalid_correct_option(instructor_session):
    """Test creating a question with an invalid correct_option"""
    course_id, week_id, assignment_id = create_test_assignment(instructor_session)


    response = instructor_session.post(ENDPOINTS["question_create"].format(assignment_id=assignment_id), data={
        "question_description": "Invalid correct option?",
        "option1": "A",
        "option2": "B",
        "option3": "C",
        "option4": "D",
        "correct_option": "5"
    })
    assert response.status_code == 400
    assert response.json()["error"] == "Correct option must be between 1 and 4"
    delete_test_assignment(instructor_session, course_id, week_id, assignment_id)

def test_get_questions(instructor_session):
    """Test fetching all questions for an assignment"""
    course_id, week_id, assignment_id, question_id = create_test_question(instructor_session)

    response = instructor_session.get(ENDPOINTS["question_list"].format(assignment_id=assignment_id))
    assert response.status_code == 200
    assert len(response.json()["questions"]) > 0
    delete_test_question(instructor_session, course_id, week_id, assignment_id, question_id)

def test_get_questions_invalid_assignment(instructor_session):
    """Test fetching questions for an invalid assignment_id"""
    response = instructor_session.get(ENDPOINTS["question_list"].format(assignment_id=9999))
    assert response.status_code == 404
    assert response.json()["error"] == "Invalid assignment_id"

def test_delete_question(instructor_session):
    """Test instructor successfully deleting a question"""
    course_id, week_id, assignment_id, question_id = create_test_question(instructor_session)
    delete_test_question(instructor_session, course_id, week_id, assignment_id, question_id)

def test_delete_question_unauthorized(student_session, instructor_session):
    """Test unauthorized user (student) attempting to delete a question"""
    course_id, week_id, assignment_id, question_id = create_test_question(instructor_session)
    response = student_session.delete(ENDPOINTS["question_delete"].format(question_id=question_id))
    assert response.status_code == 403
    assert response.json()["error"] == "Access denied. Only instructors can delete questions."
    delete_test_question(instructor_session, course_id, week_id, assignment_id, question_id)

def test_delete_nonexistent_question(instructor_session):
    """Test deleting a non-existent question"""
    response = instructor_session.delete(ENDPOINTS["question_delete"].format(question_id=9999))
    assert response.status_code == 404
    assert response.json()["error"] == "Invalid question_id"
