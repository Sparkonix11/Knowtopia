import requests
import os
import json
from pathlib import Path

# Base URL for API endpoints
BASE_URL = "http://127.0.0.1:5000/api/v1"

# User credentials
INSTRUCTOR_EMAIL = "instructor@mail.com"
INSTRUCTOR_PASSWORD = "password@123"

# Course details
COURSE_NAME = "sample course"
COURSE_DESCRIPTION = "sample course description"
COURSE_THUMBNAIL = "course_demo.png"

# Week details
WEEK_NAME = "demo week 1"

# Material details
MATERIAL1_NAME = "demo video"
MATERIAL1_DURATION = "7"
MATERIAL1_FILE = "demo_video.mp4"

MATERIAL2_NAME = "demo pdf"
MATERIAL2_DURATION = "5"
MATERIAL2_FILE = "sample.pdf"


def create_users():
    """
    Create two users by sending POST requests to the signup endpoint:
    1. An instructor with email instructor@mail.com and password 'password@123'
    2. A student with email student@mail.com and password 'password@123'
    """
    print("\n===== CREATING USERS =====\n")
    signup_endpoint = f"{BASE_URL}/auth/signup"
    
    # Instructor user data
    instructor_data = {
        'email': INSTRUCTOR_EMAIL,
        'password': INSTRUCTOR_PASSWORD,
        'password_confirm': INSTRUCTOR_PASSWORD,
        'fname': 'Instructor',
        'lname': 'User',
        'is_instructor': 'true',
        'phone': '+911234567890'
    }
    
    # Student user data
    student_data = {
        'email': 'student@mail.com',
        'password': 'password@123',
        'password_confirm': 'password@123',
        'fname': 'Student',
        'lname': 'User',
        'is_instructor': 'false',
        'phone': '+919876543210'
    }
    
    # Create instructor
    print("Creating instructor user...")
    instructor_created = False
    try:
        response = requests.post(signup_endpoint, data=instructor_data)
        if response.status_code == 201:
            print("Instructor created successfully!")
            print(json.dumps(response.json(), indent=2))
            instructor_created = True
        else:
            print(f"Failed to create instructor: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error creating instructor: {str(e)}")
    
    # Create student
    print("\nCreating student user...")
    try:
        response = requests.post(signup_endpoint, data=student_data)
        if response.status_code == 201:
            print("Student created successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to create student: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error creating student: {str(e)}")
    
    return instructor_created


# Function to login and get session cookie
def login():
    print("\nLogging in as instructor...")
    login_endpoint = f"{BASE_URL}/auth/login"
    login_data = {
        'email': INSTRUCTOR_EMAIL,
        'password': INSTRUCTOR_PASSWORD
    }
    
    response = requests.post(login_endpoint, data=login_data)
    
    if response.status_code == 200:
        print("Login successful!")
        return response.cookies
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None


# Function to create a course
def create_course(cookies):
    print("\nCreating sample course...")
    create_course_endpoint = f"{BASE_URL}/course/create"
    
    # Prepare course data
    course_data = {
        'name': COURSE_NAME,
        'description': COURSE_DESCRIPTION
    }
    
    # Prepare thumbnail file
    thumbnail_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', COURSE_THUMBNAIL)
    
    files = {}
    if os.path.exists(thumbnail_path):
        files['thumbnail'] = (COURSE_THUMBNAIL, open(thumbnail_path, 'rb'), 'image/png')
    
    response = requests.post(
        create_course_endpoint, 
        data=course_data, 
        files=files, 
        cookies=cookies
    )
    
    if response.status_code == 201:
        print("Course created successfully!")
        course_data = response.json().get('course', {})
        print(f"Course ID: {course_data.get('id')}")
        return course_data.get('id')
    else:
        print(f"Failed to create course: {response.status_code}")
        print(response.text)
        return None


# Function to create a week
def create_week(course_id, cookies):
    print(f"\nCreating week for course ID {course_id}...")
    create_week_endpoint = f"{BASE_URL}/week/create/{course_id}"
    
    week_data = {
        'name': WEEK_NAME
    }
    
    response = requests.post(
        create_week_endpoint, 
        data=week_data, 
        cookies=cookies
    )
    
    if response.status_code == 201:
        print("Week created successfully!")
        week_data = response.json().get('week', {})
        print(f"Week ID: {week_data.get('id')}")
        return week_data.get('id')
    else:
        print(f"Failed to create week: {response.status_code}")
        print(response.text)
        return None


# Function to create a material
def create_material(week_id, material_name, material_duration, material_file, cookies):
    print(f"\nCreating material '{material_name}' for week ID {week_id}...")
    create_material_endpoint = f"{BASE_URL}/material/create/{week_id}"
    
    material_data = {
        'name': material_name,
        'duration': material_duration
    }
    
    # Prepare material file
    material_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', material_file)
    
    files = {}
    if os.path.exists(material_path):
        # Determine content type based on file extension
        content_type = 'application/pdf' if material_file.endswith('.pdf') else 'video/mp4'
        files['file'] = (material_file, open(material_path, 'rb'), content_type)
    else:
        print(f"Warning: Material file {material_path} does not exist!")
        return None
    
    response = requests.post(
        create_material_endpoint, 
        data=material_data, 
        files=files, 
        cookies=cookies
    )
    
    if response.status_code == 201:
        print(f"Material '{material_name}' created successfully!")
        material_data = response.json().get('material', {})
        print(f"Material ID: {material_data.get('id')}")
        return material_data.get('id')
    else:
        print(f"Failed to create material: {response.status_code}")
        print(response.text)
        return None


def create_sample_course():
    print("\n===== CREATING SAMPLE COURSE =====\n")
    # Login to get session cookies
    cookies = login()
    if not cookies:
        print("Failed to login. Exiting.")
        return False
    
    # Create course
    course_id = create_course(cookies)
    if not course_id:
        print("Failed to create course. Exiting.")
        return False
    
    # Create week
    week_id = create_week(course_id, cookies)
    if not week_id:
        print("Failed to create week. Exiting.")
        return False
    
    # Create materials
    material1_id = create_material(week_id, MATERIAL1_NAME, MATERIAL1_DURATION, MATERIAL1_FILE, cookies)
    if not material1_id:
        print("Failed to create first material.")
    
    material2_id = create_material(week_id, MATERIAL2_NAME, MATERIAL2_DURATION, MATERIAL2_FILE, cookies)
    if not material2_id:
        print("Failed to create second material.")
    
    print("\nCourse creation completed!")
    print(f"Created course '{COURSE_NAME}' with ID {course_id}")
    print(f"Created week '{WEEK_NAME}' with ID {week_id}")
    if material1_id:
        print(f"Created material '{MATERIAL1_NAME}' with ID {material1_id}")
    if material2_id:
        print(f"Created material '{MATERIAL2_NAME}' with ID {material2_id}")
    
    return True


def main():
    print("\n===== STARTING MOCK DATA CREATION =====\n")
    
    instructor_created = create_users()
    if not instructor_created:
        print("\nFailed to create instructor user. Cannot proceed with course creation.")
        return
    
    course_created = create_sample_course()
    
    if instructor_created and course_created:
        print("\n===== MOCK DATA CREATION COMPLETED SUCCESSFULLY =====\n")
    else:
        print("\n===== MOCK DATA CREATION COMPLETED WITH ERRORS =====\n")


if __name__ == "__main__":
    main()