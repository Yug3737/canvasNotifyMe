

import requests

CANVAS_BASE_URL = 'https://kent.instructure.com'
ACCESS_TOKEN = '15107~ryyMGXemnzMX3nQwAfVzKEuEH9AyLUXvuQTyCafhA8m8M2QQEQtUE3WMGEmLwHTX'

def get_courses():
    url = f"{CANVAS_BASE_URL}/api/v1/courses"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_assignments(course_id):
    url = f"{CANVAS_BASE_URL}/api/v1/courses/{course_id}/assignments"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    courses = get_courses()
    for course in courses:
        print(f"Course: {course['name']}")
        assignments = get_assignments(course['id'])
        for assignment in assignments:
            print(f" - Assignment: {assignment['name']} Due: {assignment['due_at']}")

if __name__ == "__main__":
    main()
        
