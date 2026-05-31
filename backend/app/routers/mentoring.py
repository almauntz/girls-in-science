from fastapi import APIRouter, Depends, Form, UploadFile, File, status, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.mentor import Mentor

from pydantic import BaseModel

router = APIRouter(prefix="/mentoring", tags=["mentoring"])

# POPRAVLJENO: Dodana polja koja admin stranica zahtijeva za pregled prijave
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
    # Ova tri polja su falila i rušila frontend:
    email: str | None = None
    years_of_experience: int | None = None
    cv_url: str | None = None
    # Dodana polja za MentorProfileView:
    position: str | None = None
    institution: str | None = None

    class Config:
        from_attributes = True


@router.get("/")
def mentoring_placeholder():
    return {"message": "Mentoring router is working — Team 2 builds here"}


@router.get("/mentors", response_model=list[MentorOut])
def get_mentors(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get list of approved mentors"""
    mentors = db.query(Mentor).filter(Mentor.is_approved == True).offset(skip).limit(limit).all()
    
    result = []
    for mentor in mentors:
        f_name = mentor.first_name or ""
        l_name = mentor.last_name or ""
        full_name = f"{f_name} {l_name}".strip() or "Unknown Mentor"

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
            is_available=0 < max_m,
            email=mentor.email,
            years_of_experience=mentor.years_of_experience,
            cv_url=mentor.cv_url,
            position=mentor.position,
            institution=mentor.institution
        ))
    return result


@router.post("/apply", status_code=status.HTTP_201_CREATED)
async def apply_as_mentor(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    field_of_expertise: str = Form(...),
    years_of_experience: int = Form(...),
    linkedin_url: str = Form(...),
    bio: str = Form(...),
    cv_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Mentor application endpoint - upisuje mentora na čekanje u bazu podataka."""
    
    existing_mentor = db.query(Mentor).filter(Mentor.email == email).first()
    if existing_mentor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Prijava sa ovim emailom već postoji."
        )

    cv_filename = cv_file.filename if cv_file else None

    new_mentor = Mentor(
        first_name=first_name,
        last_name=last_name,
        email=email,
        field_of_expertise=field_of_expertise,
        years_of_experience=years_of_experience,
        linkedin_url=linkedin_url,
        bio=bio,
        cv_url=cv_filename,  
        is_approved=False  
    )

    db.add(new_mentor)
    db.commit()
    db.refresh(new_mentor)

    return {
        "message": "Prijava je uspješno poslana i čeka odobrenje administratora.",
        "mentor_id": new_mentor.id
    }


@router.get("/mentors/{id}", response_model=MentorOut)
def get_mentor_profile(id: int, db: Session = Depends(get_db)):
    """Get detailed profile of a single mentor"""
    mentor = db.query(Mentor).filter(Mentor.id == id).first()
    
    if not mentor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor not found.")
    
    f_name = mentor.first_name or ""
    l_name = mentor.last_name or ""
    full_name = f"{f_name} {l_name}".strip() or "Unknown Mentor"
        
    max_m = mentor.max_mentees or 1
    
    # POPRAVLJENO: Vraćamo i email, iskustvo i CV da frontend ima šta da iscrta
    return MentorOut(
        id=mentor.id,
        full_name=full_name,
        bio=mentor.bio,
        field_of_expertise=mentor.field_of_expertise or "Not specified",
        linkedin_url=mentor.linkedin_url,
        preferred_session_format=mentor.preferred_session_format or "Online",
        max_mentees=max_m,
        current_applications_count=0,
        is_available=0 < max_m,
        email=mentor.email,
        years_of_experience=mentor.years_of_experience,
        cv_url=mentor.cv_url,
        position=mentor.position,
        institution=mentor.institution
    )