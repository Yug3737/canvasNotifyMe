import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.signupStudent import Base, Student
from database import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.signupStudent import Base, Student
from sqlalchemy.orm import DeclarativeBase
from app import app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SUPABASE_DB_URL')  
class base(DeclarativeBase):
     pass

def create_database():
     db.create_all()

db = SQLAlchemy(model_class=Base)
db.init_app(app)

def check_db():
    print("Inside check_db() func")

    # Query all students
    # students = db.session.query(Student).all()
    students = db.session.execute(db.select(Student).order_by(Student.first_name)).scalars()
    for student in students:
        print(f"ID: {student.id}, First Name: {student.first_name}, Last Name: {student.last_name}, Cell Number: {student.cell_number}, Cell Carrier: {student.cell_carrier}")


if __name__ == "__main__":
    with app.app_context():
        create_database()
        check_db()