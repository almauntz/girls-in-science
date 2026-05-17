from typing import Optional
from sqlmodel import SQLModel, Field


class Mentor(SQLModel, table=True):
    __tablename__ = "mentors"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Osnovne informacije
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    institution: Optional[str] = Field(default=None)
    position: Optional[str] = Field(default=None)
    city_country: Optional[str] = Field(default=None)
    linkedin_url: Optional[str] = Field(default=None)

    # Profesionalno iskustvo
    academic_title: Optional[str] = Field(default=None)
    field_of_expertise: str = Field(nullable=False)
    years_of_experience: Optional[str] = Field(default=None)  
    cv_url: Optional[str] = Field(default=None)
    has_mentoring_experience: Optional[bool] = Field(default=None)

    # Motivacija i dostupnost
    motivation: Optional[str] = Field(default=None)
    max_mentees: Optional[int] = Field(default=1) 
    preferred_session_format: Optional[str] = Field(default=None)

    # Postojeća polja
    bio: Optional[str] = Field(default=None)
    profile_img_url: Optional[str] = Field(default=None)
    is_approved: bool = Field(default=False)