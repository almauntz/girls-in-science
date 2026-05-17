from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.workshops_models import Workshop, WorkshopStatus, WorkshopCreate, WorkshopUpdate, WorkshopRead
from datetime import datetime, timezone
router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.get("/")
def workshops_placeholder():
    return {"message": "Workshops router is working — Team 1 builds here"}


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Samo administrator može izvršiti ovu akciju."
        )
    return current_user
   

### Admin CRUD endpoints -------------------------------------------------------


@router.post("/", response_model=WorkshopRead, status_code=status.HTTP_201_CREATED)
def create_workshop(
    data: WorkshopCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    workshop = Workshop(
        title=data.title,
        description=data.description,
        location=data.location,
        date=data.date,
        end_time=data.end_time,
        capacity=data.capacity,
        created_by_id=admin.id
    )
    db.add(workshop)
    db.commit()
    db.refresh(workshop)
    return workshop
