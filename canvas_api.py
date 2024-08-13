
# file: test.py
# author: Yug Patel
# last modified: 16 June 2024
#

import os
import requests
from datetime import datetime, timezone
from dateutil import parser
from dotenv import load_dotenv
load_dotenv()

CANVAS_BASE_URL = 'https://kent.instructure.com/api/v1'
# Yug's access token

YUG_CANVAS_ACCESS_TOKEN = os.getenv('YUG_CANVAS_ACCESS_TOKEN')

def get_headers():
    return{
        "Authorization": f"Bearer {YUG_CANVAS_ACCESS_TOKEN}"
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

def compare_date_time_obj_iso(obj1:str, obj2:str) -> str:
    obj1_date = obj1.split('T')[0]
    obj2_date = obj2.split('T')[0]
    obj1_time = obj1.split('T')[1]
    obj2_time = obj2.split('T')[1]

    result1 = f"{obj1} is before {obj2}"
    result2 = f"{obj1} is after {obj2}"
    result3 = f"{obj1} is same as {obj2}"

    obj2_year = int(obj2_date.split('-')[0])
    obj2_month = int(obj2_date.split('-')[1])
    obj2_day = int(obj2_date.split('-')[2])

    obj1_year = int(obj1_date.split('-')[0])
    obj1_month = int(obj1_date.split('-')[1])
    obj1_day = int(obj1_date.split('-')[2])

    if obj1_year > obj2_year:
        return result2 
    elif obj1_year < obj2_year:
        return result1 
    elif obj1_year == obj2_year:
        if obj1_month > obj2_month:
            return result2
        elif obj1_month < obj2_month:
            return result1
        elif obj2_month == obj1_month:
            if obj1_day > obj2_day:
                return result2
            elif obj1_day < obj2_day:
                return result1
            elif obj1_day  == obj2_day:
                
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
 
if __name__ == "__main__":
    test_profile = get_user_profile()
    test_id = test_profile.get('id')
    test_lti_user_id = test_profile.get('lti_user_id')
    test_sortable_name = test_profile.get('sortable_name')
    test_time_zone = test_profile.get('time_zone')

    test_text_number_obj = get_text_number(test_id) 
    print("test_id", test_id)
    print("test_time_zone",test_time_zone)
    print("test_sortable_name",test_sortable_name)
    print("test_lti_user_id",test_lti_user_id)

    # test_email_id = None

    for item in test_text_number_obj:
        if item['type'] == 'email':
            test_email_id= item['address']
            break
    print("test_email_id",test_email_id)
    
    print("---------------------------------------------------------")
    test_courses = get_user_courses(test_id)

    test_course_ids = []
    test_course_names = []
    
    print("test_course_ids", test_course_ids)

    problem_courses = []
    for test_course in test_courses:
        # print(test_course)
        if 'name' in test_course:
            print("test_course['name']", test_course['name'])
            if "INTERMEDIATE MACROECONOMIC" in test_course['name']:
                rw_course = test_course
        else:
            print("Key 'name' not found in test_course")
            problem_courses.append(test_course)

# print(problem_courses)
# print(rw_course)

# Now have all the detials for research writing course
def get_assignments_for_user(course_id):
    url = f"{CANVAS_BASE_URL}/courses/{course_id}/assignments/"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

rw_course_id = rw_course['id']
rw_assignments = get_assignments_for_user(rw_course_id)

rw_hw_duedates = []
rw_hw_dict = {} # dict with key as HW names and value as due datetime
for rw_assignment in rw_assignments:
    if rw_assignment['due_at'] != None:
        rw_hw_dict[rw_assignment['name']] = rw_assignment['due_at']

print(rw_hw_dict)


rw_hw_due_dates = list(rw_hw_dict.values())
# print(rw_hw_due_dates)
# print("result of comparing 2 datetime strings ->")
# print(rw_hw_due_dates[0])
# print(rw_hw_due_dates[1])
# print(compare_date_time_obj_iso(rw_hw_due_dates[0], rw_hw_due_dates[1]))

# Finding latest current time object
# precondition: given the OS is working
# postcondition: returns a string represented in the format "YYYY-MM-DDTDD-MM-SSz"
def get_current_time_string()-> str:
    curr_time_obj = datetime.now()
    time_string = curr_time_obj.strftime('%Y-%m-%dT%H:%M:%S')
    return time_string

# precondition: given 2 strings first is due date of a HW and second is current time,
#               both in the formats of "YYYY-MM-DDTDD-MM-SSz"
# postcondition: returns the approximate difference between the date and hours of the two dates 
#                as an int
def get_approximate_duedate_difference(duedate: str, today: str) -> int:
    # Parse the date strings into datetime objects
    duedate_dt = datetime.strptime(duedate, '%Y-%m-%dT%H:%M:%Sz')
    today_dt = datetime.strptime(today, '%Y-%m-%dT%H:%M:%Sz')
    
    # Calculate the difference in days
    difference = (duedate_dt - today_dt).days
    return difference
        
# print(get_approximate_duedate_difference('2024-02-08T14:25:00z','2024-01-30T14:25:00z'))

# precondition: parameters are current time string and homeworks dictionary with keys are homework names and 
#               values are corresponding hw names
# postcondition: returns a filtered dictionary whose homework due dates are within 14 days of current date 
def get_hws_due(hw_dict: dict, current_time: str) -> dict:
    result_dict = {}
    for hw, due_date in hw_dict.items():
        # print("before for loop---------------------------------")
        if get_approximate_duedate_difference(due_date, current_time) < 14 and \
        get_approximate_duedate_difference(due_date, current_time) > 0:
            result_dict[hw] = due_date
            print(result_dict[hw])
    return result_dict
print("--------------------------------------------------------")
print("rw_hw_dict",rw_hw_dict)
print(get_hws_due(rw_hw_dict,"2024-04-01T13:25:00z")) 

if __name__ == "__main__":
    pass