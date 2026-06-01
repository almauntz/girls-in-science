from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from app.database import get_db
from app.models.mentor import Mentor, ApplicationStatus
from app.models.student import Student
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.schemas.mentor import MentorApplicationOut, RejectApplicationRequest

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"]
)


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can access this resource"
        )
    return current_user


@router.get("/mentor-applications", response_model=List[MentorApplicationOut])
def get_mentor_applications(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    query = db.query(Mentor)
    if status:
        query = query.filter(Mentor.status == status)
    applications = query.offset(skip).limit(limit).all()
    return applications


@router.patch("/mentor-applications/{id}/approve", response_model=MentorApplicationOut)
def approve_mentor_application(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    mentor = db.query(Mentor).filter(Mentor.id == id).first()
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mentor application with id {id} not found"
        )
    mentor.is_approved = True
    mentor.status = ApplicationStatus.APPROVED
    mentor.rejection_reason = None

    # Automatski promijeni rolu u users tabeli
    user = db.query(User).filter(User.email == mentor.email).first()
    if user:
        user.role = UserRole.mentor

    db.commit()
    db.refresh(mentor)
    return mentor


@router.patch("/mentor-applications/{id}/reject", response_model=MentorApplicationOut)
def reject_mentor_application(
    id: int,
    body: Optional[RejectApplicationRequest] = Body(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    mentor = db.query(Mentor).filter(Mentor.id == id).first()
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mentor application with id {id} not found"
        )
    mentor.is_approved = False
    mentor.status = ApplicationStatus.REJECTED
    mentor.rejection_reason = body.rejection_reason if body else None

    # Vrati rolu na member u users tabeli
    user = db.query(User).filter(User.email == mentor.email).first()
    if user:
        user.role = UserRole.member

    db.commit()
    db.refresh(mentor)
    return mentor


@router.patch("/mentor-applications/{id}/resubmit", response_model=MentorApplicationOut)
def resubmit_mentor_application(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    mentor = db.query(Mentor).filter(Mentor.id == id).first()
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mentor application with id {id} not found"
        )
    mentor.status = ApplicationStatus.PENDING
    mentor.is_approved = False
    mentor.rejection_reason = None
    db.commit()
    db.refresh(mentor)
    return mentor


@router.delete("/mentor-applications/{id}", status_code=status.HTTP_200_OK)
def delete_mentor_application(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    mentor = db.query(Mentor).filter(Mentor.id == id).first()
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mentor application with id {id} not found"
        )
    db.delete(mentor)
    db.commit()
    return {"message": f"Mentor application {id} successfully deleted"}


@router.get("/mentor-applications/{id}", response_model=MentorApplicationOut)
def get_mentor_application_detail(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    mentor = db.query(Mentor).filter(Mentor.id == id).first()
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prijava sa ID-em {id} nije pronađena."
        )
    return mentor


# ========================================
# STUDENT APLIKACIJE - Admin panel
# ========================================

class StudentApplicationOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    faculty: Optional[str] = None
    year_of_study: Optional[str] = None
    areas_of_interest: Optional[str] = None
    expectations: Optional[str] = None
    motivational_message: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


@router.get("/student-applications", response_model=List[StudentApplicationOut])
def get_pending_student_applications(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    applications = (
        db.query(Student)
        .filter(Student.status == ApplicationStatus.PENDING)
        .order_by(Student.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return applications


@router.get("/student-applications/{id}", response_model=StudentApplicationOut)
def get_student_application_detail(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student aplikacija sa ID-em {id} nije pronađena."
        )
    return student


@router.patch("/student-applications/{id}/approve", response_model=StudentApplicationOut)
def approve_student_application(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student aplikacija sa ID-em {id} nije pronađena."
        )
    student.status = ApplicationStatus.APPROVED
    db.commit()
    db.refresh(student)
    return student


@router.patch("/student-applications/{id}/reject", response_model=StudentApplicationOut)
def reject_student_application(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student aplikacija sa ID-em {id} nije pronađena."
        )
    student.status = ApplicationStatus.REJECTED
    db.commit()
    db.refresh(student)
    return student


@router.delete("/student-applications/{id}")
def delete_student_application(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student aplikacija sa ID-em {id} nije pronađena."
        )
    db.delete(student)
    db.commit()
    return {"message": f"Student aplikacija sa ID-em {id} je obrisana."}


@router.get("/student-applications-approved", response_model=List[StudentApplicationOut])
def get_approved_student_applications(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    applications = (
        db.query(Student)
        .filter(Student.status == ApplicationStatus.APPROVED)
        .order_by(Student.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return applications


@router.get("/student-applications-rejected", response_model=List[StudentApplicationOut])
def get_rejected_student_applications(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    applications = (
        db.query(Student)
        .filter(Student.status == ApplicationStatus.REJECTED)
        .order_by(Student.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return applications