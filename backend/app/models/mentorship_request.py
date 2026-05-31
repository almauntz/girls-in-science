import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
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
    expectations = Column(String, nullable=False)
    skills_to_improve = Column(String, nullable=False)
    cv_file_path = Column(String, nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False)