#
# file: test.py
# author: Yug Patel
# last modified: 16 June 2024
#

import requests

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
    url = f"{CANVAS_BASE_URL}/users/{user_id}/courses"
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

    test_email_id = None
    print(test_email_id)

    for item in test_text_number_obj:
        if item['type'] == 'email':
            test_email_id= item['address']
            break
    
    # phone_numbers = []
    # for channel in test_text_number_obj:
        # if channel['type'] in ['sms', 'phone']:
            # phone_numbers.append(channel['address'])
    # print(phone_numbers) 

    print("---------------------------------------------------------")
    test_courses = get_user_courses(test_id)

    test_course_ids = []
    test_course_names = []
    for course in test_courses:
       test_course_ids.append(course['id'])
       test_course_names.append(course['name']) 
    
    print(test_course_names)
    print(test_course_ids)
    # print(test_courses)