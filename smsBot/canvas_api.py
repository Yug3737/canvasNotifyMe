
# file: canvas_api.py
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

CANVAS_ACCESS_TOKEN = os.getenv('CANVAS_ACCESS_TOKEN')

def get_headers():
    return{
        "Authorization": f"Bearer {CANVAS_ACCESS_TOKEN}"
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
    result1 = f"{obj1} is before {obj2}"
    result2 = f"{obj1} is after {obj2}"
    result3 = f"{obj1} is same as {obj2}"

    obj1_date = obj1.split('T')[0]
    obj2_date = obj2.split('T')[0]
    obj1_time = obj1.split('T')[1]
    obj2_time = obj2.split('T')[1]

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

def get_assignments_by_course_id(course_id):
    url = f"{CANVAS_BASE_URL}/courses/{course_id}/assignments/"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

# Finding latest current time object
# precondition: given the OS is working
# postcondition: returns a string represented in the format "YYYY-MM-DDTDD-MM-SSz"
def get_current_time_string_iso()-> str:
    curr_time_obj = datetime.now()
    time_string = curr_time_obj.strftime('%Y-%m-%dT%H:%M:%S')
    time_string += "z"
    return time_string

# precondition: given 2 strings first is due date of a HW and second is current time,
#               both in the formats of "YYYY-MM-DDTDD-MM-SSz"
# postcondition: returns the approximate difference between the date and hours of the two dates as an int
def get_approximate_duedate_difference(duedate: str, today: str) -> int:
    duedate_dt = datetime.strptime(duedate, '%Y-%m-%dT%H:%M:%Sz')
    today_dt = datetime.strptime(today, '%Y-%m-%dT%H:%M:%Sz')
    difference = (duedate_dt - today_dt).days
    return difference

def get_curr_month(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    return date.month

def get_curr_year(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    return date.year

def get_curr_semester_course_name_id_dict(user_id):
    curr_month = get_curr_month(get_current_time_string_iso())
    curr_season, curr_year = "", str(get_curr_year(get_current_time_string_iso()))
    if 8 <= curr_month <= 12:
        curr_season = "Fall "
    elif 1 <= curr_month <= 5:
        curr_season = "Spring "
    else:
        curr_season = "Summer "
    
    curr_semester = curr_season + curr_year

    courses = get_user_courses(user_id)
    curr_semester_course_id_name_dict = {}
    for course in courses:
        if 'name' in course:
            course_name = course['name']
            if curr_semester in course_name:
                curr_semester_course_id_name_dict[course['id']] = course_name
    return curr_semester_course_id_name_dict

def get_hw_dict_from_course_ids(user_id):
    course_name_id_dict = get_curr_semester_course_name_id_dict(user_id)
    hw_dict = {}
    for course_id in course_name_id_dict.keys():
        hws = get_assignments_by_course_id(course_id)
        try:
            course_name = course_name_id_dict[course_id]
            course_name = course_name.split("(")[0]
            course_name = course_name.split(" ")[2:]
            course_name = " ".join(course_name)
            hw_name = course_name + hws[0]['name']
            hw_due_at =hws[0]['due_at']
            hw_dict[hw_name] = hw_due_at
        except Exception:
            pass
    return hw_dict

# MAIN
if __name__ == "__main__":
    user_profile = get_user_profile()
    user_id = user_profile.get('id')
    lti_user_id = user_profile.get('lti_user_id')
    sortable_name = user_profile.get('sortable_name')
    time_zone = user_profile.get('time_zone')

    hw_dict = get_hw_dict_from_course_ids(user_id)
    print(get_hws_due(hw_dict, get_current_time_string_iso()))
    print("---------------------------------------------------------")
