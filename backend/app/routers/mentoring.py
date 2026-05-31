from fastapi import APIRouter, Depends, Form, UploadFile, File, status, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.student import Student
import os
import shutil


from app.models.mentor import Mentor
from app.models.mentorship_request import MentorshipRequest, RequestStatus
from pydantic import BaseModel
from datetime import datetime
import os
import shutil
import uuid

router = APIRouter(prefix="/mentoring", tags=["mentoring"])

CV_UPLOAD_DIR = "uploads/cv"
os.makedirs(CV_UPLOAD_DIR, exist_ok=True)

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
    email: str | None = None
    years_of_experience: int | None = None
    cv_url: str | None = None
    position: str | None = None
    institution: str | None = None

    class Config:
        from_attributes = True


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


@router.get("/test")
def test_endpoint():
    return {"status": "OK", "message": "Test endpoint works"}


@router.get("/mentors")
def get_mentors(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        print("DEBUG: Starting get_mentors")
        print(f"DEBUG: db session type: {type(db)}")
        mentors = db.query(Mentor).offset(skip).limit(limit).all()
        print(f"DEBUG: Found {len(mentors)} mentors")
        result = []
        for mentor in mentors:
            result.append({
                "id": mentor.id,
                "first_name": mentor.first_name,
                "last_name": mentor.last_name,
                "email": mentor.email,
                "field_of_expertise": mentor.field_of_expertise
            })
        print("DEBUG: Returning result")
        return result
    except Exception as e:
        import traceback
        error_msg = str(e)
        tb = traceback.format_exc()
        print(f"ERROR in get_mentors: {error_msg}")
        print(f"TRACEBACK: {tb}")
        return {
            "error": error_msg,
            "traceback": tb,
            "type": str(type(e))
        }


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
        "mentor_id": new_mentor.id,
        "first_name": new_mentor.first_name,
        "email": new_mentor.email
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


@router.post("/students/register", status_code=status.HTTP_201_CREATED)
async def register_student(
    full_name: str = Form(...),
    email: str = Form(...),
    university: str = Form(None),
    faculty: str = Form(None),
    year_of_study: str = Form(None),
    city_country: str = Form(None),
    areas_of_interest: str = Form(None),
    has_business_idea: str = Form(None),
    expectations: str = Form(None),
    skills_to_improve: str = Form(None),
    preferred_session_format: str = Form(None),
    session_commitment: bool = Form(False),
    consent_data: bool = Form(False),
    consent_evaluation: bool = Form(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Student).filter(Student.email == email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prijava sa ovim emailom već postoji."
        )

    student = Student(
        full_name=full_name,
        email=email,
        university=university,
        faculty=faculty,
        year_of_study=year_of_study,
        city_country=city_country,
        areas_of_interest=areas_of_interest,
        has_business_idea=has_business_idea,
        expectations=expectations,
        skills_to_improve=skills_to_improve,
        preferred_session_format=preferred_session_format,
        session_commitment=session_commitment,
        consent_data=consent_data,
        consent_evaluation=consent_evaluation
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {"message": "Prijava uspješno poslana!", "id": student.id}
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
    valid_statuses = ["PENDING", "APPROVED", "REJECTED"]
    if request.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status mora biti jedan od: {', '.join(valid_statuses)}"
        )
    application.status = RequestStatus[request.status]
    db.commit()
    db.refresh(application)
    return {
        "message": f"Zahtjev je uspješno ažuriran na status: {request.status}",
        "application_id": application.id,
        "status": application.status.value
    }
