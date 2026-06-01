import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class MentorshipRequest(Base):
    __tablename__ = "mentorship_requests"

    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("mentors.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # UKLONJENO: student_user_id - duplikat od student_id
    expectations = Column(String, nullable=False)
    skills_to_improve = Column(String, nullable=False)
    cv_file_path = Column(String, nullable=False)
    message = Column(Text, nullable=False)  # nullable=False
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    student = relationship("User", foreign_keys=[student_id])
    mentor = relationship("Mentor", foreign_keys=[mentor_id])