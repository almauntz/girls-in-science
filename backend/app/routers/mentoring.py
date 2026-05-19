from fastapi import APIRouter, Depends, Query, HTTPException, Form, UploadFile, File, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.mentor import Mentor
from app.models.mentor_application import MentorApplication, ApplicationStatus
import os
import re
from pathlib import Path
from datetime import datetime

router = APIRouter(prefix="/mentoring", tags=["mentoring"])

# --- Pydantic Schemas ---

class MentorApplicationRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    field_of_expertise: str
    years_of_experience: int
    linkedin_url: str
    bio: str


class MentorApplicationResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    field_of_expertise: str
    years_of_experience: int
    linkedin_url: str
    bio: str
    cv_url: str
    status: str
    created_at: str

    class Config:
        from_attributes = True


def validate_linkedin_url(url: str) -> bool:
    """Validate LinkedIn URL format"""
    linkedin_pattern = r'^https?://(?:www\.)?linkedin\.com/.*'
    return bool(re.match(linkedin_pattern, str(url)))


def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    allowed_extensions = {'.pdf', '.docx'}
    return os.path.splitext(filename)[1].lower() in allowed_extensions

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

@router.get("/mentors")
def get_mentors(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    mentors = db.query(Mentor)\
                .filter(Mentor.is_approved == True)\
                .offset(skip)\
                .limit(limit)\
                .all()
    return mentors


@router.post("/apply", response_model=MentorApplicationResponse, status_code=status.HTTP_201_CREATED)
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
    """
    Public endpoint for mentor applications.
    Accepts multipart/form-data with text fields and CV document.
    """
    try:
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Check if email already exists in applications
        existing_application = db.query(MentorApplication).filter(
            MentorApplication.email == email
        ).first()
        
        if existing_application:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already submitted an application"
            )
        
        # Validate LinkedIn URL
        if not validate_linkedin_url(linkedin_url):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid LinkedIn URL format. Please use a valid LinkedIn profile URL"
            )
        
        # Validate file extension
        if not is_allowed_file(cv_file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF and DOCX files are allowed"
            )
        
        # Validate file size (max 5MB)
        file_size = await cv_file.file.seek(0, 2)  # Seek to end
        await cv_file.file.seek(0)  # Reset to beginning
        if file_size > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 5MB"
            )
        
        # Generate unique filename based on email and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        email_safe = email.split('@')[0]
        file_extension = os.path.splitext(cv_file.filename)[1].lower()
        unique_filename = f"{email_safe}_{timestamp}{file_extension}"
        
        # Define upload path
        upload_dir = Path("uploads/mentors/cvs")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / unique_filename
        
        # Save file to disk
        contents = await cv_file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Create database record
        relative_cv_path = str(file_path).replace("\\", "/")
        
        mentor_app = MentorApplication(
            first_name=first_name,
            last_name=last_name,
            email=email,
            field_of_expertise=field_of_expertise,
            years_of_experience=years_of_experience,
            linkedin_url=str(linkedin_url),
            bio=bio,
            cv_url=relative_cv_path,
            status=ApplicationStatus.pending
        )
        
        db.add(mentor_app)
        db.commit()
        db.refresh(mentor_app)
        
        return {
            **mentor_app.__dict__,
            "status": mentor_app.status.value,
            "created_at": mentor_app.created_at.isoformat() if mentor_app.created_at else None
        }
    
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists in our system"
        )
    except Exception as e:
        db.rollback()
        # Clean up uploaded file if database save fails
        try:
            if file_path and file_path.exists():
                file_path.unlink()
        except:
            pass
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process application: {str(e)}"
        )