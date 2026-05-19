from pydantic import BaseModel
from typing import Optional
from app.models.mentor import ApplicationStatus


class MentorApplicationOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    institution: Optional[str] = None
    position: Optional[str] = None
    city_country: Optional[str] = None
    linkedin_url: Optional[str] = None
    
    academic_title: Optional[str] = None
    field_of_expertise: str
    years_of_experience: Optional[int] = None
    cv_url: Optional[str] = None
    has_mentoring_experience: Optional[bool] = None
    
    motivation: Optional[str] = None
    max_mentees: Optional[int] = 1
    preferred_session_format: Optional[str] = None
    
    bio: Optional[str] = None
    profile_img_url: Optional[str] = None
    is_approved: bool
    status: ApplicationStatus

    class Config:
        from_attributes = True