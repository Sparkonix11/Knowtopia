import requests
from tests import ENDPOINTS

def test_get_user_profile(student_session):
    """Test retrieving the user's profile"""
    response = student_session.get(ENDPOINTS["user_profile"])
    assert response.status_code == 200
    assert "user" in response.json()
    assert "email" in response.json()["user"]

def test_update_user_profile(student_session):
    """Test updating the user's profile details"""
    updated_data = {
        "fname": "UpdatedFirstName",
        "lname": "UpdatedLastName",
        "phone": "9999999999"
    }
    response = student_session.put(ENDPOINTS["user_profile"], data=updated_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Profile updated successfully"
    assert response.json()["user"]["fname"] == "UpdatedFirstName"
    assert response.json()["user"]["lname"] == "UpdatedLastName"
    assert response.json()["user"]["phone"] == "9999999999"

def test_update_user_profile_invalid_dob(student_session):
    """Test updating profile with an invalid date of birth format"""
    response = student_session.put(ENDPOINTS["user_profile"], data={"dob": "31-02-2025"})
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid date format. Please use DD-MM-YYYY."

def test_update_user_profile_invalid_image(student_session):
    """Test uploading an unsupported image format"""
    invalid_image = {
        "image": ("invalid_file.txt", b"dummy content", "text/plain")
    }
    response = student_session.put(ENDPOINTS["user_profile"], files=invalid_image)
    assert response.status_code == 400
    assert response.json()["error"] == "File type not allowed"

def test_update_password_correct(student_session):
    """Test updating password with correct current password"""
    password_data = {
        "current_password": "oldpassword",
        "new_password": "newsecurepassword"
    }
    response = student_session.put(ENDPOINTS["user_profile"], data=password_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Profile updated successfully"

def test_update_password_wrong(student_session):
    """Test updating password with incorrect current password"""
    password_data = {
        "current_password": "wrongpassword",
        "new_password": "newsecurepassword"
    }
    response = student_session.put(ENDPOINTS["user_profile"], data=password_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Current password is incorrect"

def test_get_user_profile_unauthenticated():
    """Test accessing user profile without authentication"""
    response = requests.get(ENDPOINTS["user_profile"])
    assert response.status_code == 401  # Unauthorized
