from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.mentor import Mentor, ApplicationStatus
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.schemas.mentor import MentorApplicationOut

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
def get_pending_mentor_applications(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    applications = (
        db.query(Mentor)
        .filter(Mentor.status == ApplicationStatus.PENDING)
        .offset(skip)
        .limit(limit)
        .all()
    )
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
    db.commit()
    db.refresh(mentor)
    return mentor


@router.patch("/mentor-applications/{id}/reject", response_model=MentorApplicationOut)
def reject_mentor_application(
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
    mentor.is_approved = False
    mentor.status = ApplicationStatus.REJECTED
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
    """
    Dohvata sve detalje jedne specifične prijave za mentorstvo.
    Ovo se koristi kada admin klikne 'Pregledaj'.
    """
    mentor = db.query(Mentor).filter(Mentor.id == id).first()
    
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prijava sa ID-em {id} nije pronađena."
        )
    
    return mentor