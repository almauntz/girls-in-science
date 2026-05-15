from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.workshops_models import Workshop, WorkshopDetailRead, WorkshopStatus, WorkshopCreate, WorkshopUpdate, WorkshopRead, WorkshopList
from datetime import datetime, timezone

router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.get("/")
def workshops_placeholder():
    return {"message": "Workshops router is working — Team 1 builds here"}

@router.get("/active", response_model=list[WorkshopList])
def get_active_workshops(
    db: Session = Depends(get_db)
):
    statement = select(Workshop).where(
        Workshop.status == WorkshopStatus.upcoming,
        Workshop.date >= datetime.now(timezone.utc)
    ).order_by(
        Workshop.date,
        Workshop.title)
    workshops = db.exec(statement).all()
    if not workshops:
        raise HTTPException(status_code=404, detail="Nema aktivnih radionica.")
    return workshops

@router.get("/{workshop_id}", response_model=WorkshopDetailRead)
def get_workshop_details(workshop_id: int, db: Session = Depends(get_db)):
    workshop = db.get(Workshop, workshop_id)
    if not workshop:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena.")
    organizer = db.get(User, workshop.created_by_id)
    return WorkshopDetailRead(
        ID_workshop=workshop.ID_workshop,
        title=workshop.title,
        description=workshop.description,
        date=workshop.date,
        end_time=workshop.end_time,
        capacity=workshop.capacity,
        status=workshop.status,
        organizer_name=organizer.full_name,
        organizer_email=organizer.email
    )

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


@router.patch("/{workshop_id}", response_model=WorkshopRead)
def update_workshop(
    workshop_id: int,
    data: WorkshopUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    workshop = db.get(Workshop, workshop_id)
    if not workshop:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena.")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(workshop, key, value)

    db.add(workshop)
    db.commit()
    db.refresh(workshop)
    return workshop


@router.patch("/{workshop_id}/cancel", response_model=WorkshopRead)
def cancel_workshop(
    workshop_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    workshop = db.get(Workshop, workshop_id)
    if not workshop:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena.")
    if workshop.status == WorkshopStatus.cancelled:
        raise HTTPException(status_code=400, detail="Radionica je već otkazana.")

    workshop.status = WorkshopStatus.cancelled
    db.add(workshop)
    db.commit()
    db.refresh(workshop)
    return workshop


@router.delete("/{workshop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workshop(
    workshop_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    workshop = db.get(Workshop, workshop_id)
    if not workshop:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena.")

    db.delete(workshop)
    db.commit()
