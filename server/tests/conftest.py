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