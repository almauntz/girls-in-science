from sqlalchemy import Column, Integer, String
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    faculty = Column(String, nullable=True)
    year_of_study = Column(String, nullable=True)
    areas_of_interest = Column(String, nullable=True)  # čuvamo kao comma-separated string
    motivational_message = Column(String, nullable=True)
    expectations = Column(String, nullable=True)
    skills_to_improve = Column(String, nullable=True)
    preferred_session_format = Column(String, nullable=True)
    cv_url = Column(String, nullable=True)