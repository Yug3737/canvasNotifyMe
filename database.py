from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.signupStudent import Base, Student
import os

SUPABASE_DB_URL = os.getenv('SUPABASE_DB_URL')
engine = create_engine(os.getenv('SUPABSE_DB_URL'))
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    pass