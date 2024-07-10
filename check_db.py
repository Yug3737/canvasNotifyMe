from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.signupStudent import Base, Student
from database import session

def check_db():
    print("Inside check_db() func")

    # Query all students
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.id}, First Name: {student.first_name}, Last Name: {student.last_name}, Cell Number: {student.cell_number}, Cell Carrier: {student.cell_carrier}")


if __name__ == "__main__":
    check_db()