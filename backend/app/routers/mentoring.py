from fastapi import APIRouter, Depends, Form, UploadFile, File, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/mentoring", tags=["mentoring"])

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
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get list of approved mentors"""
    # TODO: Implement mentor listing when your team builds this
    return []


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
    """
    Mentor application endpoint.
    TODO: Implement full mentor application logic when your team builds this
    """
    return {
        "message": "Application received. Team 2 will process this when implementation is complete.",
        "status": "pending"
    }