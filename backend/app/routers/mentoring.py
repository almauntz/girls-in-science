from fastapi import APIRouter, Depends, Form, UploadFile, File, status, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.mentor import Mentor, MentorshipRequest, RequestStatus

from pydantic import BaseModel
from datetime import datetime

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


# Schema za MentorshipRequest - što mentorica vidi
class MentorshipRequestOut(BaseModel):
    id: int
    student_user_id: int
    student_name: str
    student_email: str
    message: str
    status: str
    created_at: datetime
    
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


@router.get("/my-applications", response_model=list[MentorshipRequestOut])
def get_mentor_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mentorica vidi svoje pristigle zahtjeve od studentica.
    Pronalazi Mentor po emailu i vraća sve zahtjeve za tu mentoricu.
    """
    # Pronađi mentoricu po emailu
    mentor = db.query(Mentor).filter(Mentor.email == current_user.email).first()
    
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil mentorici nije pronađen. Trebate se prijaviti kao mentorica."
        )
    
    # Pronađi sve zahtjeve za tu mentoricu
    applications = db.query(MentorshipRequest).filter(
        MentorshipRequest.mentor_id == mentor.id
    ).order_by(MentorshipRequest.created_at.desc()).all()
    
    # Mapiranje rezultata
    result = []
    for app in applications:
        student_name = app.student.full_name if app.student else "Unknown"
        student_email = app.student.email if app.student else "unknown@example.com"
        status_value = app.status.value if isinstance(app.status, RequestStatus) else str(app.status)
        result.append(MentorshipRequestOut(
            id=app.id,
            student_user_id=app.student_user_id,
            student_name=student_name,
            student_email=student_email,
            message=app.message,
            status=status_value,
            created_at=app.created_at
        ))
    
    return result


class UpdateApplicationStatusRequest(BaseModel):
    status: str


@router.put("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    request: UpdateApplicationStatusRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mentorica ažurira status zahtjeva (APPROVED ili REJECTED)
    """
    # Pronađi aplikaciju
    application = db.query(MentorshipRequest).filter(
        MentorshipRequest.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zahtjev nije pronađen."
        )
    
    # Provjeri da li mentorica može prijaviti ovaj zahtjev
    mentor = db.query(Mentor).filter(Mentor.email == current_user.email).first()
    if not mentor or mentor.id != application.mentor_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nemate dozvolu da ažurirate ovaj zahtjev."
        )
    
    # Validacija statusa
    valid_statuses = ["PENDING", "APPROVED", "REJECTED"]
    if request.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status mora biti jedan od: {', '.join(valid_statuses)}"
        )
    
    # Ažuriranje statusa
    application.status = RequestStatus[request.status]
    db.commit()
    db.refresh(application)
    
    return {
        "message": f"Zahtjev je uspješno ažuriran na status: {request.status}",
        "application_id": application.id,
        "status": application.status.value
    }