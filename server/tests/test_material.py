import requests
from tests import ENDPOINTS
from tests.conftest import create_test_material, delete_test_material, create_test_week, delete_test_week

def test_create_material_as_instructor(instructor_session):
    """Test creating a material successfully as an instructor"""
    course_id, week_id, material_id = create_test_material(instructor_session)
    delete_test_material(instructor_session, course_id, week_id, material_id)

def test_create_material_as_non_instructor(instructor_session, student_session):
    """Test that a non-instructor cannot create materials"""
    files = {
        "file": ("example.pdf", b"dummy content", "application/pdf")
    }
    data = {
        "name": "Sample Material",
        "duration": "10"
    }
    course_id, week_id = create_test_week(instructor_session)
    response = student_session.post(ENDPOINTS["material_create"].format(week_id=week_id), files=files, data=data)
    
    assert response.status_code == 403
    assert response.json()["error"] == "User is not an instructor"
    delete_test_week(instructor_session, course_id, week_id)

def test_create_material_invalid_week(instructor_session):
    """Test creating material with an invalid week_id"""
    files = {
        "file": ("example.pdf", b"dummy content", "application/pdf")
    }
    data = {
        "name": "Invalid Week Material",
        "duration": "10"
    }
    response = instructor_session.post(ENDPOINTS["material_create"].format(week_id=999), files=files, data=data)
    
    assert response.status_code == 404
    assert response.json()["error"] == "Invalid week_id"

def test_create_material_duplicate(instructor_session):
    """Test that duplicate material names are not allowed within the same week"""
    course_id, week_id, material_id = create_test_material(instructor_session)

    files = {
        "file": ("example.pdf", b"dummy content", "application/pdf")
    }
    data = {
        "name": "Sample Material",
        "duration": "10"
    }
    response = instructor_session.post(ENDPOINTS["material_create"].format(week_id=week_id), files=files, data=data)
    
    assert response.status_code == 400
    assert response.json()["error"] == "Material already exists"
    delete_test_material(instructor_session, course_id, week_id, material_id)

def test_create_material_no_file(instructor_session):
    """Test that an error occurs if no file is uploaded"""
    data = {
        "name": "Material Without File",
        "duration": "10"
    }
    course_id, week_id = create_test_week(instructor_session)
    response = instructor_session.post(ENDPOINTS["material_create"].format(week_id=week_id), data=data)
    
    assert response.status_code == 400
    assert response.json()["error"] == "No file uploaded"
    delete_test_week(instructor_session, course_id, week_id)

def test_create_material_invalid_file_type(instructor_session):
    """Test uploading an invalid file type"""
    files = {
        "file": ("invalid.exe", b"dummy content", "application/octet-stream")
    }
    data = {
        "name": "Invalid File Material",
        "duration": "10"
    }
    course_id, week_id = create_test_week(instructor_session)
    response = instructor_session.post(ENDPOINTS["material_create"].format(week_id=week_id), files=files, data=data)
    
    assert response.status_code == 400
    assert response.json()["error"] == "File type not allowed"
    delete_test_week(instructor_session, course_id, week_id)

def test_create_material_unauthenticated(student_session, instructor_session):
    """Test that unauthenticated users cannot create materials"""
    files = {
        "file": ("example.pdf", b"dummy content", "application/pdf")
    }
    data = {
        "name": "Unauthenticated Material",
        "duration": "10"
    }
    course_id, week_id = create_test_week(instructor_session)
    response = student_session.post(ENDPOINTS["material_create"].format(week_id=week_id), files=files, data=data)
    delete_test_week(instructor_session, course_id, week_id)
    
    assert response.status_code == 403  # Unauthorized

def test_delete_material_as_instructor(instructor_session):
    """Test deleting a material successfully as an instructor"""
    course_id, week_id, material_id = create_test_material(instructor_session)
    delete_test_material(instructor_session, course_id, week_id, material_id)

def test_delete_material_as_non_instructor(instructor_session, student_session):
    """Test that a non-instructor cannot delete materials"""
    course_id, week_id, material_id = create_test_material(instructor_session)

    response = student_session.delete(ENDPOINTS["material_delete"].format(material_id=material_id))
    
    assert response.status_code == 403
    assert response.json()["error"] == "User is not an instructor"
    delete_test_material(instructor_session, course_id, week_id, material_id)

def test_delete_material_not_found(instructor_session):
    """Test trying to delete a non-existent material"""
    response = instructor_session.delete(ENDPOINTS["material_delete"].format(material_id=999))
    
    assert response.status_code == 404
    assert response.json()["error"] == "Material not found"

# def test_delete_material_not_owner(instructor_session_other):
#     """Test that an instructor cannot delete materials they did not create"""
#     response = instructor_session_other.delete(ENDPOINTS["material_delete"].format(material_id=1))
    
#     assert response.status_code == 403
#     assert response.json()["error"] == "User is not the creator of the course"

def test_delete_material_unauthenticated():
    """Test that unauthenticated users cannot delete materials"""
    response = requests.delete(ENDPOINTS["material_delete"].format(material_id=1))
    
    assert response.status_code == 401  # Unauthorized
