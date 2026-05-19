import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.database import Base


class ApplicationStatus(str, enum.Enum):
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
    years_of_experience = Column(String, nullable=True)
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