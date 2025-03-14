import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

ENDPOINTS = {
    "assignment": f"{BASE_URL}/assignment/{{assignment_id}}",
    "create_assignment": f"{BASE_URL}/assignment/create/{{week_id}}",
    "delete_assignment": f"{BASE_URL}/assignment/delete/{{assignment_id}}",
    
    "signup": f"{BASE_URL}/auth/signup",
    "login": f"{BASE_URL}/auth/login",
    "logout": f"{BASE_URL}/auth/logout",

    "course": f"{BASE_URL}/course",
    "create_course": f"{BASE_URL}/course/create",
    "instructor_courses": f"{BASE_URL}/course/instructor",
    "delete_course": f"{BASE_URL}/course/delete/{{course_id}}",
    "enrolled_courses": f"{BASE_URL}/course/enrolled",
    "enroll_student": f"{BASE_URL}/course/enroll/{{course_id}}/{{student_id}}",

    "material_create": f"{BASE_URL}/material/create/{{week_id}}",
    "material_delete": f"{BASE_URL}/material/delete/{{material_id}}",

    "question_create": f"{BASE_URL}/question/create/{{assignment_id}}",
    "question_list": f"{BASE_URL}/question/{{assignment_id}}",
    "question_delete": f"{BASE_URL}/question/delete/{{question_id}}",

    "review": f"{BASE_URL}/review/{{material_id}}",
    "review_delete": f"{BASE_URL}/review/delete/{{review_id}}",

    "user_profile": f"{BASE_URL}/user",
    "user_students": f"{BASE_URL}/user/students",
    "user_delete": f"{BASE_URL}/user/delete/{{user_id}}",

    "week_create": f"{BASE_URL}/week/create/{{course_id}}",
    "week_delete": f"{BASE_URL}/week/delete/{{course_id}}/{{week_id}}",

    "ask": f"{BASE_URL}/ask",
    "question_hint": f"{BASE_URL}/question_hint"
}
