from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.mentor import Mentor



router = APIRouter(prefix="/mentoring", tags=["mentoring"])

class MentorOut(BaseModel):
    id: int
    full_name: str
    bio: str | None = None
    field_of_expertise: str
    linkedin_url: str | None = None
    preferred_session_format: str | None = None
    max_mentees: int
    current_applications_count: int
    is_available: bool

    class Config:
        from_attributes = True


# -------------------------------------------------------
# Team 2 — Mentoring
# This is your router. All your endpoints go here.
#
# Example protected endpoint:
#
# @router.get("/")
# def get_mentors(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

@router.get("/")
def mentoring_placeholder():
    return {"message": "Mentoring router is working — Team 2 builds here"}

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.mentor import Mentor
from pydantic import BaseModel

router = APIRouter(prefix="/mentoring", tags=["mentoring"])


@router.get("/")
def mentoring_placeholder():
    return {"message": "Mentoring router is working — Team 2 builds here"}

@router.get("/mentors", response_model=list[MentorOut])
def get_mentors(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    mentors = db.query(Mentor).filter(Mentor.is_approved == True).offset(skip).limit(limit).all()
    
    result = []
    for mentor in mentors:
        full_name = f"{mentor.first_name or ''} {mentor.last_name or ''}".strip() or "Unknown Mentor"
        max_m = mentor.max_mentees or 1
        result.append(MentorOut(
            id=mentor.id,
            full_name=full_name,
            bio=mentor.bio,
            field_of_expertise=mentor.field_of_expertise or "Not specified",
            linkedin_url=mentor.linkedin_url,
            preferred_session_format=mentor.preferred_session_format or "Online",
            max_mentees=max_m,
            current_applications_count=0,
            is_available=0 < max_m
        ))
    return result

@router.get("/mentors/{id}", response_model=MentorOut)
def get_mentor_profile(id: int, db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.id == id).first()
    
    if not mentor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor not found.")
    
    full_name = f"{mentor.first_name or ''} {mentor.last_name or ''}".strip() or "Unknown Mentor"
    max_m = mentor.max_mentees or 1
    
    return MentorOut(
        id=mentor.id,
        full_name=full_name,
        bio=mentor.bio,
        field_of_expertise=mentor.field_of_expertise or "Not specified",
        linkedin_url=mentor.linkedin_url,
        preferred_session_format=mentor.preferred_session_format or "Online",
        max_mentees=max_m,
        current_applications_count=0,
        is_available=0 < max_m
    )