from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.workshops_models import Workshop,RegistrationCreate,Registration, WorkshopStatus, WorkshopCreate, WorkshopUpdate, WorkshopRead, WorkshopList,WorkshopDetailRead
from datetime import datetime, timezone
from sqlalchemy import func
router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.get("/")
def workshops_placeholder():
    return {"message": "Workshops router is working — Team 1 builds here"}
@router.get("/active", response_model=list[WorkshopList])
def get_active_workshops(db: Session = Depends(get_db)):
    # 1. Uzimamo sve radionice koje su 'upcoming'
    statement = select(Workshop).where(Workshop.status == WorkshopStatus.upcoming).order_by(Workshop.date)
    workshops = db.execute(statement).scalars().all()
    
    result = []
    
    for w in workshops:
        # 2. Brojimo prijave koristeći .execute i .scalar() (ovo rješava tvoj AttributeError)
        broj_prijava = db.execute(
            select(func.count(Registration.id)).where(Registration.workshop_id == w.ID_workshop)
        ).scalar() or 0
        
        # 3. Pretvaramo model iz baze u rječnik da bismo mu dodali polje koje ne postoji u bazi
        workshop_dict = w.model_dump()
        
        # 4. Izračunavamo slobodna mjesta
        workshop_dict["free_spots"] = w.capacity - broj_prijava
        
        result.append(workshop_dict)

    # 5. Vraćamo listu rječnika koju će FastAPI automatski pretvoriti u WorkshopList objekte
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
        organizer_name=organizer.full_name,
        organizer_email=organizer.email,
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
    current_user: User = Depends(get_current_user) # Ovo štiti rutu!
):
    radionica = db.get(Workshop, podaci.workshop_id)

    if not radionica:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena")


 #Provjera da li je student već prijavljen na radionicu (preko emaila)
    postojeca = db.exec(
        select(Registration).where(
            Registration.workshop_id == podaci.workshop_id,
            Registration.email == podaci.email
        )
    ).first()

    if postojeca:
        raise HTTPException(
            status_code=400,
            detail="Already registered with this email"
        )
    

    # Kapacitet (brojanje)
    broj_prijava = db.execute(
        select(func.count(Registration.id)).where(Registration.workshop_id == podaci.workshop_id)
    ).scalar() or 0

    
    if broj_prijava >= radionica.capacity:
        raise HTTPException(status_code=400, detail="Nažalost, sva mjesta su popunjena!")
    # 4. Kreiranje prijave
    nova_prijava = Registration(**podaci.model_dump())

    db.add(nova_prijava)
    db.commit()
    db.refresh(nova_prijava)

    preostalo = radionica.capacity - (broj_prijava + 1)
    
    return {
        "message": "Uspješna prijava!",
        "free_spots_left": max(0, preostalo) 
    }


@router.delete("/cancellation/{registration_id}")
def cancel_registration(registration_id: int, db: Session = Depends(get_db)):
    prijava = db.get(Registration, registration_id)
    if not prijava:
        raise HTTPException(status_code=404, detail="Prijava nije pronađena")

    db.delete(prijava)
    db.commit()

    return {"message": "Uspješno ste se odjavili. Mjesto je sada slobodno."}



@router.get("/prijava/status/{workshop_id}")
def provjeri_status_prijave(
    workshop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.exec(
        select(Registration).where(
            Registration.ID_workshop == workshop_id,
            Registration.user_id == current_user.id
        )
    ).first()

    if existing:
        return {"status": "Prijavljena"}

    return {"status": "Ne prijavljena"}