import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/v1/course"  #Change if needed

@pytest.fixture
def instructor_session():
    #For Logging as an instructor and returning a session
    session = requests.Session()
    login_data = {
        "email": "dummyinst@ds.study.iitm.ac.in",  #instructor email (KINDLY FIRST REGISTER)
        "password": "dummyPass@2"
    }
    response = session.post(f"http://127.0.0.1:5000/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    return session  #Returns authenticated session

def test_get_all_courses():
    #Test for retrieving all the courses
    response = requests.get(f"{BASE_URL}/all")
    assert response.status_code == 200
    print(response.json())
    assert "courses" in response.json()


def test_get_instructor_courses(instructor_session):
    #Test for retrieving instructor-specific courses
    response = instructor_session.get(f"{BASE_URL}/instructor_courses")
    assert response.status_code == 200
    
    #assert response.status_code in [200, 403]  # 403 if not an instructor

def test_create_course(instructor_session):
    #Test for creating a new course as an instructor
    course_data = {
        "name": "Instructor Course Test1",
        "description": "A course by James Bond"
    }
    response = instructor_session.post(f"{BASE_URL}/create", data=course_data)
    assert response.status_code == 201
    assert response.json()["message"] == "Course Created"

def test_delete_course(instructor_session):
    #Test for deleting a course (only by the instructor)
    course_data = {
        "name": "Test Course created to delete",
        "description": "This course will be deleted"
    }
    response = instructor_session.post(f"{BASE_URL}/create", data=course_data)
    assert response.status_code == 201
    course_id = response.json()["course"]["id"]
    response = instructor_session.delete(f"{BASE_URL}/{course_id}/delete")
    assert response.status_code == 200
    assert response.json()["message"] == "Course deleted"
    #assert response.status_code in [200, 403, 404]  # 403 if not authorized, 404 if course not found

def test_create_course_with_missing_fields(instructor_session):
    #Test for creating a new course as an instructor with some required field missing
    course_data = {
        "name": "Instructor Course Test with missing description",
        #Missing description
    }
    response = instructor_session.post(f"{BASE_URL}/create", data=course_data)
    assert response.status_code == 400
    assert response.json()["message"] == "Missing required fields"


#------Checked for unauthorized user access------


@pytest.fixture
def student_session():
    #For Logging as a student and returning session for student user
    session = requests.Session()
    login_data = {
        "email": "dummyuser@ds.study.iitm.ac.in",  #student email
        "password": "dummyPass@1"
    }
    response = session.post(f"http://127.0.0.1:5000/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    return session  #Returns authenticated session

def test_create_course_u(student_session):
    #Test for creating a new course as a student user
    course_data = {
        "name": "Student Course Test1",
        "description": "A course by Unauthorized user"
    }
    response = student_session.post(f"{BASE_URL}/create", data=course_data)
    assert response.status_code == 403
    assert response.json()["message"] == "User is not an instructor" 
