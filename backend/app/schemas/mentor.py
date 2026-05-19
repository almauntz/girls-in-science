from pydantic import BaseModel
from typing import Optional
from app.models.mentor import ApplicationStatus


class MentorApplicationOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    field_of_expertise: str
    bio: Optional[str] = None
    profile_img_url: Optional[str] = None
    institution: Optional[str] = None
    position: Optional[str] = None
    city_country: Optional[str] = None
    is_approved: bool
    status: ApplicationStatus

    class Config:
        from_attributes = True
