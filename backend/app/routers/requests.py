import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.mentorship_request import MentorshipRequest, RequestStatus

from app.models.student import Student



router = APIRouter(
    prefix="/mentoring/requests",
    tags=["requests"],
    redirect_slashes=False  
)

#kreiranje direktorijuma za čuvanje CV-ova ako ne postoji
UPLOAD_DIR = "storage/cv"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_request(
    mentor_id: int = Form(...),
    expectations: str = Form(...),
    skills_to_improve: str = Form(...),
    cv: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.student import Student

    student = db.query(Student).filter(Student.email == current_user.email).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Samo registrovane studentice mogu slati zahtjeve za mentorstvo."
        )
    #validacija fajla
    if cv.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dozvoljen je isključivo PDF format."
        )

    # citanje sadržaja fajla i provjera veličine
    contents = await cv.read()
    max_file_size = 5 * 1024 * 1024  # Konverzija 5MB u bajtove
    
    if len(contents) > max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fajl ne smije biti veći od 5MB."
        )

    # generisanje jedinstvenog imena fajla 
    unique_filename = str(uuid.uuid4()) + "_" + cv.filename
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    #spašavanje fajla na disk
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    #kreiranje objekta i upisivanje u bazu podataka
    # Provjeri da li već postoji zahtjev od ovog studenta prema ovom mentoru
    existing_request = db.query(MentorshipRequest).filter(
        MentorshipRequest.mentor_id == mentor_id,
        MentorshipRequest.student_id == current_user.id,
        MentorshipRequest.status == RequestStatus.PENDING
    ).first()
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Već postoji aktivan zahtjev prema ovom mentoru."
        )

    new_request = MentorshipRequest(
        mentor_id=mentor_id,
        student_id=current_user.id,
        expectations=expectations,
        skills_to_improve=skills_to_improve,
        cv_file_path=file_path,
        status=RequestStatus.PENDING
    )
    
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return {
        "message": "Zahtjev je uspješno poslan.",
        "request_id": new_request.id,
        "status": new_request.status
    }