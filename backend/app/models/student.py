import enum
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Enum
from datetime import datetime
from app.database import Base


class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DELETED = "DELETED"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    # Lični podaci
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    faculty = Column(String, nullable=True)
    year_of_study = Column(String, nullable=True)

    # Akademski interesi
    areas_of_interest = Column(String, nullable=True)
    has_business_idea = Column(String, nullable=True)  # "Da", "Ne", "Other"

    # Očekivanja
    expectations = Column(String, nullable=True)
    skills_to_improve = Column(String, nullable=True)
    motivational_message = Column(Text, nullable=True)

    # Dostupnost
    preferred_session_format = Column(String, nullable=True)
    session_commitment = Column(Boolean, default=False)

    # Saglasnosti
    consent_data = Column(Boolean, default=False)
    consent_evaluation = Column(Boolean, default=False)
    
    # CV datoteka
    cv_url = Column(String, nullable=True)
    
    # Status i timestamp
    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.PENDING,
        nullable=False,
        server_default=ApplicationStatus.PENDING.value
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)