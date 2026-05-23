from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.workshops_models import Workshop,RegistrationCreate,Registration, WorkshopStatus, WorkshopCreate, WorkshopUpdate, WorkshopRead, WorkshopList,WorkshopDetailRead
from datetime import datetime, timezone
from sqlalchemy import func
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlmodel import select
router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.delete("/cancellation/{workshop_id}")
def cancel_registration(
    workshop_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Tražimo prijavu na osnovu ID-a radionice i email-a ulogovanog korisnika
    # Pošto tvoj Registration model ima 'email', ovo će raditi!
    statement = select(Registration).where(
        Registration.workshop_id == workshop_id,
        Registration.email == current_user.email
    )
    
    result = db.execute(statement).scalars().first()
    
    if not result:
        raise HTTPException(
            status_code=404, 
            detail="Nije pronađena vaša prijava za ovu radionicu."
        )
    
    db.delete(result)
    db.commit()
    
    return {"message": "Uspješno ste odustali od radionice."}





@router.get("/active", response_model=list[WorkshopList])
def get_active_workshops(db: Session = Depends(get_db)):
    statement = select(Workshop)
    workshops = db.execute(statement).scalars().all()
    result = []
    for w in workshops:
        broj_prijava = db.execute(
            select(func.count(Registration.id)).where(Registration.workshop_id == w.ID_workshop)
        ).scalar() or 0
        workshop_dict = w.model_dump()
        workshop_dict["free_spots"] = w.capacity - broj_prijava
        result.append(workshop_dict)
    return result

@router.get("/{workshop_id}", response_model=WorkshopDetailRead)
def get_workshop_details(workshop_id: int, db: Session = Depends(get_db)):
    workshop = db.get(Workshop, workshop_id)
    if not workshop:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena.")
    organizer = db.get(User, workshop.created_by_id)
    registrations = db.execute(
        select(Registration).where(Registration.workshop_id == workshop_id)
    ).all()
    free_spots = workshop.capacity - len(registrations)
    return WorkshopDetailRead(
        ID_workshop=workshop.ID_workshop,
        title=workshop.title,
        description=workshop.description,
        location=workshop.location,
        date=workshop.date,
        end_time=workshop.end_time,
        capacity=workshop.capacity,
        status=workshop.status,
        free_spots=free_spots
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


@router.post("/registration", status_code=status.HTTP_201_CREATED)
def register_student(
    podaci: RegistrationCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    radionica = db.get(Workshop, podaci.workshop_id)
    if not radionica:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena")

    broj_prijava = db.execute(
        select(func.count(Registration.id)).where(
            Registration.workshop_id == podaci.workshop_id
        )
    ).scalar() or 0
    if broj_prijava >= radionica.capacity:
        raise HTTPException(status_code=400, detail="Nažalost, sva mjesta su popunjena!")

    # 
    postojeca = db.execute(
        select(Registration).where(
            Registration.workshop_id == podaci.workshop_id,
            func.lower(Registration.email) == podaci.email.lower().strip()
        )
    ).scalars().first()
    if postojeca:
        raise HTTPException(status_code=400, detail="Već ste prijavljeni na ovu radionicu!")

    
    nova_prijava = nova_prijava = Registration(
    **podaci.model_dump(),
    user_id=current_user.id
)

    db.add(nova_prijava)
    db.commit()
    db.refresh(nova_prijava)

    preostalo = radionica.capacity - (broj_prijava + 1)

    return {
        "message": "Uspješna prijava!",
        "free_spots_left": max(0, preostalo)
    }

@router.delete("/cancellation/{workshop_id}")
def cancel_registration(
    workshop_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Tražimo prijavu na osnovu ID-a radionice i email-a ulogovanog korisnika
    # Pošto tvoj Registration model ima 'email', ovo će raditi!
    statement = select(Registration).where(
        Registration.workshop_id == workshop_id,
        Registration.email == current_user.email
    )
    
    result = db.execute(statement).scalars().first()
    
    if not result:
        raise HTTPException(
            status_code=404, 
            detail="Nije pronađena vaša prijava za ovu radionicu."
        )
    
    db.delete(result)
    db.commit()
    
    return {"message": "Uspješno ste odustali od radionice."}