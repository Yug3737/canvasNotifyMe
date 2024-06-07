#
# file: test.py
# author: Yug Patel
# last modified: 26 May 2024
#

import requests

CANVAS_BASE_URL = 'https://kent.instructure.com/api/v1'
ACCESS_TOKEN = '15107~ryyMGXemnzMX3nQwAfVzKEuEH9AyLUXvuQTyCafhA8m8M2QQEQtUE3WMGEmLwHTX'

def get_headers():
    return{
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

def get_user_profile():
    url = f"{CANVAS_BASE_URL}/users/self/profile"
    response = requests.get(url, headers= get_headers())
    response.raise_for_status()
    return response.json()

def get_courses():
    url = f"{CANVAS_BASE_URL}/courses"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def get_course_notification(course_id):
    url = f"{CANVAS_BASE_URL}/courses/{course_id}/discussion_topics"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

 
