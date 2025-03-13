import requests
import pytest

BASE_URL = "http://127.0.0.1:5000/api/v1/assignment"
sample_week_id = 1

@pytest.fixture
def instructor_session():
    #For Logging as an instructor and returning a session
    session = requests.Session()
    login_data = {
        "email": "dummyinst@ds.study.iitm.ac.in",
        "password": "dummyPass@2"
    }
    response = session.post(f"http://127.0.0.1:5000/api/v1/auth/login", data=login_data)
    assert response.status_code == 200, "Login failed Instructor"
    return session

@pytest.fixture
def student_session():
    #For Logging as a student and returning session for student user
    session = requests.Session()
    login_data = {
        "email": "dummyuser@ds.study.iitm.ac.in",
        "password": "dummyPass@1"
    }
    response = session.post(f"http://127.0.0.1:5000/api/v1/auth/login", data=login_data)
    assert response.status_code == 200, "Login failed as Student"
    return session

def test_create_assignment(instructor_session):
    #Test to create an assignment as an instructor
    data = {
        "name": "Course1 Assignment",
        "description": "This assignment is created by instructor1"
    }
    response = instructor_session.post(f"{BASE_URL}/{sample_week_id}/create", data=data)
    assert response.status_code == 201
    json_response = response.json()
    print("Response:", json_response)
    assert "assignment" in json_response

def test_create_assignment_u(student_session):
    #Test for an Unauthorized creation of course assignments
    data = {
        "name": "Fake Assignment",
        "description": "Assignment creation attempt by an Unauthorized user"
    }
    response = student_session.post(f"{BASE_URL}/{sample_week_id}/create", data=data)
    assert response.status_code == 403
    assert response.json()["message"] == "Access denied. Only instructors can create assignments"

def test_create_assignment_missing_fields(instructor_session):
    #Test to create an assignment with missing required fields
    data = {
        "name": "Assignment with missing required fields"
    }
    response = instructor_session.post(f"{BASE_URL}/{sample_week_id}/create", data=data)
    assert response.status_code == 400
    assert response.json()["message"] == "Missing required fields"


def test_get_assignment(instructor_session):
    #Testing to retrieve an assignment
    response = instructor_session.get(f"{BASE_URL}/1/")
    assert response.status_code == 200, "Failed to retrieve assignment"
    json_response = response.json()
    print("Get Assignment Response:", json_response)
    assert "assignment" in json_response

def test_get_assignment_not_found(instructor_session):
    #Testing to retrieve an assignment that doesn't exist
    response = instructor_session.get(f"{BASE_URL}/1234/")
    assert response.status_code == 404
    assert response.json()["message"] == "Assignment not found"


def test_delete_assignment(instructor_session):
    #Test to delete an assignment by the instructor
    response = instructor_session.delete(f"{BASE_URL}/1/delete")
    assert response.status_code == 200
    assert response.json()["message"] == "Assignment deleted"

def test_delete_assignment_unauthorized(student_session):
    #Test for an Unauthorized deletion of the assignments
    response = student_session.delete(f"{BASE_URL}/1/delete")
    assert response.status_code == 403
    assert response.json()["message"] == "Access denied. Only instructors can delete assignments"

