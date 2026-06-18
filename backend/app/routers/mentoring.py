from fastapi import APIRouter, Depends, Form, UploadFile, File, status, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.mentor import Mentor
from app.models.profile import Profile
from app.models.mentorship_request import MentorshipRequest, RequestStatus
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid
import os
import shutil

router = APIRouter(prefix="/mentoring", tags=["mentoring"])

CV_UPLOAD_DIR = "uploads/cv"
os.makedirs(CV_UPLOAD_DIR, exist_ok=True)

class MentorOut(BaseModel):
    id: int
    full_name: str
    bio: Optional[str] = None
    field_of_expertise: str
    linkedin_url: Optional[str] = None
    preferred_session_format: Optional[str] = None
    max_mentees: int
    current_applications_count: int
    is_available: bool
    email: Optional[str] = None
    years_of_experience: Optional[int] = None
    cv_url: Optional[str] = None
    position: Optional[str] = None
    institution: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class MentorshipRequestOut(BaseModel):
    id: int
    student_user_id: Optional[int] = None
    student_name: str
    student_email: str
    message: str = ""
    status: str
    created_at: datetime
    expectations: Optional[str] = None
    skills_to_improve: Optional[str] = None
    cv_file_path: Optional[str] = None
    rejection_reason: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("/")
def mentoring_placeholder():
    return {"message": "Mentoring router is working — Team 2 builds here"}

def get_avatar_url(mentor: Mentor, db: Session) -> str | None:
    user = db.query(User).filter(User.email == mentor.email).first()
    if not user:
        return mentor.profile_img_url  # fallback na vlastitu sliku
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not profile or not profile.avatar:
        return mentor.profile_img_url  # fallback
    return f"http://localhost:8000{profile.avatar}"

@router.get("/mentors", response_model=list[MentorOut])
def get_mentors(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    mentors = db.query(Mentor).filter(Mentor.is_approved == True).offset(skip).limit(limit).all()
    result = []
    for mentor in mentors:
        f_name = mentor.first_name or ""
        l_name = mentor.last_name or ""
        full_name = f"{f_name} {l_name}".strip() or "Unknown Mentor"
        max_m = mentor.max_mentees or 1
        # compute accepted requests count dynamically
        accepted_count = db.query(MentorshipRequest).filter(
            MentorshipRequest.mentor_id == mentor.id,
            MentorshipRequest.status == RequestStatus.ACCEPTED
        ).count()
        result.append(MentorOut(
            id=mentor.id,
            full_name=full_name,
            bio=mentor.bio,
            field_of_expertise=mentor.field_of_expertise or "Not specified",
            linkedin_url=mentor.linkedin_url,
            preferred_session_format=mentor.preferred_session_format or "Online",
            max_mentees=max_m,
            current_applications_count=accepted_count,
            is_available=accepted_count < max_m,
            email=mentor.email,
            years_of_experience=mentor.years_of_experience,
            cv_url=mentor.cv_url,
            position=mentor.position,
            institution=mentor.institution,
            avatar_url=get_avatar_url(mentor, db)
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
    existing_mentor = db.query(Mentor).filter(Mentor.email == email).first()
    if existing_mentor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prijava sa ovim emailom već postoji."
        )

    file_extension = os.path.splitext(cv_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(CV_UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(cv_file.file, buffer)

    new_mentor = Mentor(
        first_name=first_name,
        last_name=last_name,
        email=email,
        field_of_expertise=field_of_expertise,
        years_of_experience=years_of_experience,
        linkedin_url=linkedin_url,
        bio=bio,
        cv_url=unique_filename,
        is_approved=False
    )

    db.add(new_mentor)
    db.commit()
    db.refresh(new_mentor)

    return {
        "message": "Prijava je uspješno poslana i čeka odobrenje administratora.",
        "mentor_id": new_mentor.id
    }


@router.get("/cv/{filename}")
def download_cv(filename: str):
    file_path = os.path.join(CV_UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV fajl nije pronađen."
        )
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )


@router.get("/mentors/{id}", response_model=MentorOut)
def get_mentor_profile(id: int, db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.id == id).first()
    if not mentor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor not found.")
    f_name = mentor.first_name or ""
    l_name = mentor.last_name or ""
    full_name = f"{f_name} {l_name}".strip() or "Unknown Mentor"
    max_m = mentor.max_mentees or 1
    accepted_count = db.query(MentorshipRequest).filter(
        MentorshipRequest.mentor_id == mentor.id,
        MentorshipRequest.status == RequestStatus.ACCEPTED
    ).count()
    return MentorOut(
        id=mentor.id,
        full_name=full_name,
        bio=mentor.bio,
        field_of_expertise=mentor.field_of_expertise or "Not specified",
        linkedin_url=mentor.linkedin_url,
        preferred_session_format=mentor.preferred_session_format or "Online",
        max_mentees=max_m,
        current_applications_count=accepted_count,
        is_available=accepted_count < max_m,
        email=mentor.email,
        years_of_experience=mentor.years_of_experience,
        cv_url=mentor.cv_url,
        position=mentor.position,
        institution=mentor.institution,
        avatar_url=get_avatar_url(mentor, db)
    )



@router.get("/my-applications", response_model=list[MentorshipRequestOut])
def get_mentor_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mentor = db.query(Mentor).filter(Mentor.email == current_user.email).first()
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil mentorici nije pronađen."
        )
    applications = db.query(MentorshipRequest).filter(
        MentorshipRequest.mentor_id == mentor.id
    ).order_by(MentorshipRequest.created_at.desc()).all()

    result = []
    for app in applications:
        student_name = app.student.full_name if app.student else "Unknown"
        student_email = app.student.email if app.student else "unknown@example.com"
        status_value = app.status.value if isinstance(app.status, RequestStatus) else str(app.status)
        student_user_id = app.student_id

        result.append(MentorshipRequestOut(
            id=app.id,
            student_user_id=student_user_id,
            student_name=student_name,
            student_email=student_email,
            message=app.message or "",
            status=status_value,
            created_at=app.created_at,
            expectations=app.expectations or "",
            skills_to_improve=app.skills_to_improve or "",
            cv_file_path=app.cv_file_path or "",
            rejection_reason=app.rejection_reason or ""
        ))
    return result


class UpdateApplicationStatusRequest(BaseModel):
    status: str
    rejection_reason: Optional[str] = None


@router.put("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    request: UpdateApplicationStatusRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    application = db.query(MentorshipRequest).filter(
        MentorshipRequest.id == application_id
    ).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zahtjev nije pronađen."
        )
    mentor = db.query(Mentor).filter(Mentor.email == current_user.email).first()
    if not mentor or mentor.id != application.mentor_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nemate dozvolu da ažurirate ovaj zahtjev."
        )
    valid_statuses = ["PENDING", "ACCEPTED", "REJECTED"]
    if request.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status mora biti jedan od: {', '.join(valid_statuses)}"
        )
    # Ako prihvaćamo zahtjev, provjeri kapacitet mentora
    if request.status == "ACCEPTED":
        accepted_count = db.query(MentorshipRequest).filter(
            MentorshipRequest.mentor_id == application.mentor_id,
            MentorshipRequest.status == RequestStatus.ACCEPTED
        ).count()
        mentor_obj = db.query(Mentor).filter(Mentor.id == application.mentor_id).first()
        max_m = mentor_obj.max_mentees or 1
        if accepted_count >= max_m:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mentor je već popunjen. Ne možete prihvatiti ovaj zahtjev."
            )

    # Postavi novi status
    application.status = RequestStatus[request.status]

    # Ako se zahtjev odbija, spremi razlog odbijanja
    if request.status == "REJECTED" and request.rejection_reason:
        application.rejection_reason = request.rejection_reason
    
    db.commit()
    db.refresh(application)
    return {
        "message": f"Zahtjev je uspješno ažuriran na status: {request.status}",
        "application_id": application.id,
        "status": application.status.value
    }
