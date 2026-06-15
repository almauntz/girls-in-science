from fastapi import APIRouter, Depends, Form, UploadFile, File, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from pydantic import BaseModel
from pathlib import Path
import os

router = APIRouter(prefix="/api/v1/students", tags=["students"])

# Pydantic schema
class StudentOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    faculty: str | None = None
    year_of_study: str | None = None
    areas_of_interest: str | None = None
    motivational_message: str | None = None
    preferred_session_format: str | None = None
    cv_url: str | None = None

    class Config:
        from_attributes = True


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=StudentOut)
async def register_student(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    faculty: str = Form(...),
    year_of_study: str = Form(...),
    areas_of_interest: str = Form(...),
    expectations: str = Form(...),
    motivational_message: str = Form(...),
    preferred_session_format: str = Form(default="Online"),
    session_commitment: str = Form(default="false"),  # Primj kao string
    has_business_idea: str = Form(default=""),
    skills_to_improve: str = Form(default=""),
    consent_data: str = Form(default="false"),  # Primj kao string
    consent_evaluation: str = Form(default="false"),  # Primj kao string
    cv_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Studentica prijava endpoint - sačuva prijavu u bazu"""
    
    try:
        # Konvertuj string boolean vrednosti
        session_commitment_bool = session_commitment.lower() in ["true", "1", "on", "yes"]
        consent_data_bool = consent_data.lower() in ["true", "1", "on", "yes"]
        consent_evaluation_bool = consent_evaluation.lower() in ["true", "1", "on", "yes"]
        
        # Provjera da li email već postoji
        existing_student = db.query(Student).filter(Student.email == email).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student sa ovim emailom već postoji."
            )
        
        # Sačuvaj CV datoteku ako je poslana
        cv_url = None
        if cv_file and cv_file.filename:
            # Kreiraj folder ako ne postoji
            upload_dir = Path("storage/cv")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # Spremi datoteku sa jedinstvenim imenom (sprječava path traversal)
            import uuid
            safe_filename = f"{uuid.uuid4()}_{Path(cv_file.filename).name}"
            file_path = upload_dir / safe_filename
            with open(file_path, "wb") as buffer:
                content = await cv_file.read()
                buffer.write(content)
            
            cv_url = str(file_path)
        
        # Kreiraj novi Student objekat
        new_student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            faculty=faculty,
            year_of_study=year_of_study,
            areas_of_interest=areas_of_interest,
            expectations=expectations,
            skills_to_improve=skills_to_improve,
            motivational_message=motivational_message,
            preferred_session_format=preferred_session_format,
            session_commitment=session_commitment_bool,
            has_business_idea=has_business_idea,
            consent_data=consent_data_bool,
            consent_evaluation=consent_evaluation_bool,
            cv_url=cv_url
        )
        
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        
        return new_student
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )


@router.get("/", response_model=list[StudentOut])
def get_students(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get list of registered students"""
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


@router.get("/{id}", response_model=StudentOut)
def get_student(id: int, db: Session = Depends(get_db)):
    """Get student profile by ID"""
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student nije pronađen"
        )
    return student
