#
# file: test.py
# author: Yug Patel
# last modified: 16 June 2024
#

import requests
from datetime import datetime
from dateutil import parser

CANVAS_BASE_URL = 'https://kent.instructure.com/api/v1'
# Yug's access token
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

def get_user_courses(user_id):
    url = f"{CANVAS_BASE_URL}/users/{user_id}/courses?enrollment_state=active,invited_or_pending&per_page=100"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def get_course_notification(course_id):
    url = f"{CANVAS_BASE_URL}/courses/{course_id}/discussion_topics"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def get_text_number(given_id):
    url = f"{CANVAS_BASE_URL}/users/{given_id}/communication_channels"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()
 
if __name__ == "__main__":
    test_profile = get_user_profile()
    test_id = test_profile.get('id')
    test_lti_user_id = test_profile.get('lti_user_id')
    test_sortable_name = test_profile.get('sortable_name')
    test_time_zone = test_profile.get('time_zone')

    test_text_number_obj = get_text_number(test_id) 
    print(test_id)
    print(test_time_zone)
    print(test_sortable_name)
    print(test_lti_user_id)

    # test_email_id = None

    for item in test_text_number_obj:
        if item['type'] == 'email':
            test_email_id= item['address']
            break
    print(test_email_id)
    
    print("---------------------------------------------------------")
    test_courses = get_user_courses(test_id)

    test_course_ids = []
    test_course_names = []
    
    print(test_course_ids)

    problem_courses = []
    for test_course in test_courses:
        # print(test_course)
        if 'name' in test_course:
            print(test_course['name'])
            if "RESEARCH WRITING" in test_course['name']:
                rw_course = test_course
        else:
            print("Key 'name' not found in test_course")
            problem_courses.append(test_course)

print(problem_courses)
print(rw_course)

# Now have all the detials for research writing course
def get_assignments_for_user(course_id):
    url = f"{CANVAS_BASE_URL}/courses/{course_id}/assignments/"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

rw_course_id = rw_course['id']
rw_assignments = get_assignments_for_user(rw_course_id)
# print(rw_assignments)
print(len(rw_assignments))

rw_hw_duedates = []
rw_hw_dict = {} # dict with key as HW names and value as due datetime
for rw_assignment in rw_assignments:
    if rw_assignment['due_at'] != None:
        rw_hw_dict[rw_assignment['name']] = rw_assignment['due_at']

print(rw_hw_dict)

def get_current_time():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

for hw_name, due_date in rw_hw_dict.items():
    due_datetime_obj = datetime.fromisoformat(due_date)
    current_datetime = get_current_time()
    