from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum


class ApplicationStatus(enum.Enum):
    pending = "pending"
    reviewing = "reviewing"
    approved = "approved"
    rejected = "rejected"


class MentorApplication(Base):
    __tablename__ = "mentor_applications"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    field_of_expertise = Column(String, nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    linkedin_url = Column(String, nullable=False)
    bio = Column(Text, nullable=False)
    cv_url = Column(String, nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
