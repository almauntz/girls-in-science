import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, index=True)

    # Osnovne informacije
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    institution = Column(String, nullable=True)
    position = Column(String, nullable=True)
    city_country = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)

    # Profesionalno iskustvo
    academic_title = Column(String, nullable=True)
    field_of_expertise = Column(String, nullable=False)
    years_of_experience = Column(Integer, nullable=True)
    cv_url = Column(String, nullable=True)
    has_mentoring_experience = Column(Boolean, nullable=True)

    # Motivacija i dostupnost
    motivation = Column(String, nullable=True)
    max_mentees = Column(Integer, default=1)
    preferred_session_format = Column(String, nullable=True)

    # Ostalo
    bio = Column(String, nullable=True)
    profile_img_url = Column(String, nullable=True)
    is_approved = Column(Boolean, default=False)
    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.PENDING,
        nullable=False,
        server_default=ApplicationStatus.PENDING.value
    )


class MentorshipRequest(Base):
    __tablename__ = "mentorship_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    mentor_id = Column(Integer, ForeignKey("mentors.id"), nullable=False, index=True)
    message = Column(Text, nullable=False)
    status = Column(
        Enum(RequestStatus),
        default=RequestStatus.PENDING,
        nullable=False,
        server_default=RequestStatus.PENDING.value
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    student = relationship("User", foreign_keys=[student_user_id])
    mentor = relationship("Mentor", foreign_keys=[mentor_id])