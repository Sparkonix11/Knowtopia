import pytest
import requests
from tests import ENDPOINTS

@pytest.fixture
def valid_user():
    return {
        "email": "dummyuser@mail.com",
        "password": "dummyPass@1",
        "password_confirm": "dummyPass@1",
        "fname": "Dummy",
        "lname": "User",
        "is_instructor": "false",
        "phone": "+911234567890"
    }

@pytest.fixture(scope="session")
def create_test_users():
    """Ensure test users exist before running tests."""
    users = [
        {
            "email": "instructor@mail.com",
            "password": "password123",
            "password_confirm": "password123",
            "fname": "Instructor",
            "lname": "User",
            "is_instructor": "true"
        },
        {
            "email": "student@mail.com",
            "password": "password123",
            "password_confirm": "password123",
            "fname": "Student",
            "lname": "User",
            "is_instructor": "false"
        }
    ]

    for user in users:
        response = requests.post(ENDPOINTS["signup"], data=user, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        # If user already exists, ignore 400 errors
        if response.status_code not in [201, 400]:  
            pytest.fail(f"Failed to create test user {user['email']}: {response.json().get('error', 'Unknown error')}")

@pytest.fixture
def instructor_session(create_test_users):
    """Login as Instructor after ensuring user exists."""
    session = requests.Session()
    login_data = {
        "email": "instructor@mail.com",
        "password": "password123"
    }
    response = session.post(ENDPOINTS["login"], data=login_data)
    assert response.status_code == 200, f"Login failed for Instructor: {response.json().get('error', 'Unknown error')}"
    return session

@pytest.fixture
def student_session(create_test_users):
    """Login as Student after ensuring user exists."""
    session = requests.Session()
    login_data = {
        "email": "student@mail.com",
        "password": "password123"
    }
    response = session.post(ENDPOINTS["login"], data=login_data)
    assert response.status_code == 200, f"Login failed for Student: {response.json().get('error', 'Unknown error')}"
    return session

def create_test_course(instructor_session, name="Test Course", description="Test course description"):
    """Helper function to create a test course"""
    course_data = {
        "name": name,
        "description": description
    }
    response = instructor_session.post(ENDPOINTS["create_course"], data=course_data)
    assert response.status_code == 201
    return response.json()["course"]["id"]

def delete_test_course(instructor_session, course_id):
    """Helper function to delete a test course"""
    response = instructor_session.delete(ENDPOINTS["delete_course"].format(course_id=course_id))
    assert response.status_code == 200
    assert response.json()["message"] == "Course deleted"
    return response.json()

def create_test_week(instructor_session, name="Test Week"):
    """Helper function to create a test week"""
    course_id = create_test_course(instructor_session, "Test Course for Week Creation", 
                                  "A course to test week creation")

    week_data = {"name": name}
    response = instructor_session.post(ENDPOINTS["week_create"].format(course_id=course_id), data=week_data)
    assert response.status_code == 201
    assert response.json()["message"] == "Week created"
    
    return course_id, response.json()["week"]["id"]

def delete_test_week(instructor_session, course_id, week_id):
    """Helper function to delete a test week"""
    response = instructor_session.delete(ENDPOINTS["week_delete"].format(course_id=course_id, week_id=week_id))
    assert response.status_code == 200
    assert response.json()["message"] == "Week deleted"
    
    delete_test_course(instructor_session, course_id)
    return response.json()

def create_test_assignment(instructor_session, name="Test Assignment", description="A test assignment"):
    """Helper function to create a test assignment"""
    data = {
        "name": name,
        "description": description,
    }
    course_id, week_id = create_test_week(instructor_session)
    response = instructor_session.post(ENDPOINTS["create_assignment"].format(week_id=week_id), data=data)
    assert response.status_code == 201
    assert response.json()["message"] == "Assignment created"
    return course_id, week_id, response.json()["assignment"]["id"]

def delete_test_assignment(instructor_session, course_id, week_id, assignment_id):
    """Helper function to delete a test assignment"""
    response = instructor_session.delete(ENDPOINTS["delete_assignment"].format(assignment_id=assignment_id))
    assert response.status_code == 200
    assert response.json()["message"] == "Assignment deleted"
    delete_test_week(instructor_session, course_id, week_id)
    return response.json()

def create_test_question(instructor_session):
    """Helper function to create a test question"""
    data = {
        "question_description": "What is 2 + 2?",
        "option1": "1",
        "option2": "2",
        "option3": "4",
        "option4": "5",
        "correct_option": "3"
    }
    course_id, week_id, assignment_id = create_test_assignment(instructor_session)
    response = instructor_session.post(ENDPOINTS["question_create"].format(assignment_id=assignment_id), data=data)
    assert response.status_code == 201
    assert response.json()["message"] == "Question created"
    return course_id, week_id, assignment_id, response.json()["question"]["id"]

def delete_test_question(instructor_session, course_id, week_id, assignment_id, question_id):
    """Helper function to delete a test question"""
    response = instructor_session.delete(ENDPOINTS["question_delete"].format(question_id=question_id))
    assert response.status_code == 200
    assert response.json()["message"] == "Question deleted"
    delete_test_assignment(instructor_session, course_id, week_id, assignment_id)
    return response.json()

def create_test_material(instructor_session):
    """Helper function to create a test material"""
    files = {
        "file": ("example.pdf", b"dummy content", "application/pdf")
    }
    data = {
        "name": "Sample Material",
        "duration": "10"
    }
    course_id, week_id = create_test_week(instructor_session)
    response = instructor_session.post(ENDPOINTS["material_create"].format(week_id=week_id), files=files, data=data)
    
    assert response.status_code == 201
    assert response.json()["message"] == "Material created"
    return course_id, week_id, response.json()["material"]["id"]

def delete_test_material(instructor_session, course_id, week_id, material_id):
    """Helper function to delete a test material"""
    response = instructor_session.delete(ENDPOINTS["material_delete"].format(material_id=material_id))
    assert response.status_code == 200
    assert response.json()["message"] == "Material deleted"
    delete_test_week(instructor_session, course_id, week_id)
    return response.json()

def create_test_review(instructor_session, student_session):
    """Helper function to create a test review"""
    # Create a test material
    course_id, week_id, material_id = create_test_material(instructor_session)

    # Create a review for the material
    review_data = {
        "rating": "5",
        "comment": "Excellent material!"
    }
    response = student_session.post(
        ENDPOINTS["review"].format(material_id=material_id), 
        data=review_data
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Review created"
    return course_id, week_id, material_id, response.json()["review"]["id"]

def delete_test_review(instructor_session, student_session, course_id, week_id, material_id, review_id):
    """Helper function to delete a test review"""
    response = student_session.delete(ENDPOINTS["review_delete"].format(review_id=review_id))
    assert response.status_code == 200
    assert response.json()["message"] == "Review deleted successfully"
    delete_test_material(instructor_session, course_id, week_id, material_id)
    return response.json()


