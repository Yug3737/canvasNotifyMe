from fastapi import FastAPI, HTTPException
from .canvas_api import get_user_profile, get_courses, get_course_notifications

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to your personalized Canvas HW notification app"}

@app.get("/profile")
def read_user_profile():
    try:
        profile = get_user_profile()
        return profile
    except requests.HTTPError as err:
        raise HTTPException(status_code = err.response.status_code, detail = err.response.text)
    

@app.get("/courses")
def read_courses():
    try:
        courses = get_courses()
        return courses
    except requests.HTTPError as err:
        raise HTTPException(status_code = err.response.status_code, detail = err.response.text)
    