#
# file: test.py
# author: Yug Patel
# last modified: 16 June 2024
#

import requests
from datetime import datetime, timezone
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

def compare_date_time_obj_iso(obj1, obj2):
    obj1_date = obj1.split('T')[0]
    obj2_date = obj2.split('T')[0]
    obj1_time = obj1.split('T')[1]
    obj2_time = obj2.split('T')[1]
    # print(obj2_time)
    # print(obj1_time)

    result1 = f"{obj1} is before {obj2}"
    result2 = f"{obj1} is after {obj2}"
    result3 = f"{obj1} is same as {obj2}"

    # print("obj2_date", obj2_date)
    # print("obj1_date", obj1_date)
    obj2_year = int(obj2_date.split('-')[0])
    obj2_month = int(obj2_date.split('-')[1])
    obj2_date = int(obj2_date.split('-')[2])
    # print(obj2_year) 
    obj1_year = int(obj1_date.split('-')[0])
    obj1_month = int(obj1_date.split('-')[1])
    obj1_date = int(obj1_date.split('-')[2])

    # print(type(obj2_month))
    # print(obj2_month, obj2_date)
    if obj1_year > obj2_year:
        return result2 
    elif obj1_year < obj2_year:
        return result1 
    elif obj1_year == obj2_year:
        if obj1_month > obj2_date:
            return result2
        elif obj1_month < obj2_month:
            return result1
        elif obj2_month == obj1_month:
            if obj1_date > obj2_date:
                return result2
            elif obj1_date < obj2_date:
                return result1
            elif obj1_date == obj2_date:
                
                obj1_hour = obj1_time.split(':')[0]
                obj2_hour = obj2_time.split(':')[0]
                
                obj1_minute = obj1_time.split(':')[1]
                obj2_minute = obj2_time.split(':')[1]

                obj1_second = obj1_time.split(':')[2]
                obj2_second = obj2_time.split(':')[2]

                if obj1_hour > obj2_hour:
                    return result2
                elif obj1_hour < obj2_hour:
                    return result1
                else:
                    if obj1_minute > obj2_minute:
                        return result2
                    elif obj1_minute < obj1_minute:
                        return result1
                    else:
                        if obj1_second > obj2_second:
                            return result2
                        elif obj1_second < obj2_second:
                            return result1
                        return result3
                    


rw_hw_due_dates = list(rw_hw_dict.values())
print(rw_hw_due_dates)
print("result of comparing 2 datetime strings ->")
print(rw_hw_due_dates[0])
print(type(rw_hw_due_dates[0]))
print(rw_hw_due_dates[1])
print(type(rw_hw_due_dates[1]))
print(compare_date_time_obj_iso(rw_hw_due_dates[0], rw_hw_due_dates[1]))
# print(compare_date_time_obj_iso("2023-06-21T12:30:45", "2023-06-21T12:30:45"))  # Output: "2023-06-21T12:30:45 is the same as 2023-06-21T12:30:45"
# print(compare_date_time_obj_iso("2023-06-21T12:30:45", "2023-06-21T12:30:46"))  # Output: "2023-06-21T12:30:45 is before 2023-06-21T12:30:46"
# print(compare_date_time_obj_iso("2023-06-21T12:30:46", "2023-06-21T12:30:45"))  # Output: "2023-06-21T12:30:46 is after 2023-06-21T12:30:45"