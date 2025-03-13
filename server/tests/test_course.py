import pytest
import requests
from tests import ENDPOINTS

def test_get_all_courses():
    """Test retrieving all available courses"""
    response = requests.get(ENDPOINTS["course"])
    assert response.status_code == 200
    assert "courses" in response.json()

def test_get_instructor_courses(instructor_session):
    """Test retrieving courses created by the instructor"""
    response = instructor_session.get(ENDPOINTS["instructor_courses"])
    assert response.status_code == 200
    assert "courses" in response.json()

def test_create_course(instructor_session):
    """Test instructor creating a course"""
    course_data = {
        "name": "Instructor Course Test",
        "description": "A test course created by an instructor"
    }
    response = instructor_session.post(ENDPOINTS["create_course"], json=course_data)
    assert response.status_code == 201
    assert response.json()["message"] == "Course created"

def test_create_duplicate_course(instructor_session):
    """Test creating a course with a duplicate name"""
    course_data = {
        "name": "Duplicate Course Test",
        "description": "This course will be tested for duplicates"
    }
    response1 = instructor_session.post(ENDPOINTS["create_course"], json=course_data)
    assert response1.status_code == 201
    response2 = instructor_session.post(ENDPOINTS["create_course"], json=course_data)
    assert response2.status_code == 400
    assert response2.json()["error"] == "Course already exists"

def test_create_course_missing_fields(instructor_session):
    """Test creating a course with missing required fields"""
    course_data = {"name": "Missing Description Test"}  # Missing description
    response = instructor_session.post(ENDPOINTS["create_course"], json=course_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Missing required fields"

def test_delete_course(instructor_session):
    """Test instructor deleting a course they created"""
    course_data = {
        "name": "Course to Delete",
        "description": "This course will be deleted"
    }
    create_response = instructor_session.post(ENDPOINTS["create_course"], json=course_data)
    assert create_response.status_code == 201
    course_id = create_response.json()["course"]["id"]
    
    delete_response = instructor_session.delete(ENDPOINTS["delete_course"].format(course_id=course_id))
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Course deleted"

def test_delete_course_unauthorized(student_session):
    """Test unauthorized student trying to delete a course"""
    response = student_session.delete(ENDPOINTS["delete_course"].format(course_id=1))
    assert response.status_code == 403
    assert response.json()["error"] == "User is not the creator of the course"

def test_get_enrolled_courses(student_session):
    """Test retrieving courses a student is enrolled in"""
    response = student_session.get(ENDPOINTS["enrolled_courses"])
    assert response.status_code == 200
    assert "enrolled_courses" in response.json()

def test_enroll_student(instructor_session):
    """Test instructor enrolling a student in their course"""
    student_id = 2  # Ensure this student exists
    course_data = {
        "name": "Enrollment Test Course",
        "description": "Course for testing enrollment"
    }
    create_response = instructor_session.post(ENDPOINTS["create_course"], json=course_data)
    assert create_response.status_code == 201
    course_id = create_response.json()["course"]["id"]
    
    enroll_response = instructor_session.post(
        ENDPOINTS["enroll_student"].format(course_id=course_id, student_id=student_id)
    )
    assert enroll_response.status_code == 201
    assert enroll_response.json()["message"] == "Student enrolled successfully"

def test_enroll_student_unauthorized(student_session):
    """Test student trying to enroll another student (unauthorized)"""
    response = student_session.post(
        ENDPOINTS["enroll_student"].format(course_id=1, student_id=2)
    )
    assert response.status_code == 403
    assert response.json()["error"] == "Only instructors can enroll students"
