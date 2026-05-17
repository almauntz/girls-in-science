from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.workshops_models import Workshop,RegistrationCreate,Registration, WorkshopStatus, WorkshopCreate, WorkshopUpdate, WorkshopRead
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
        Workshop.status == WorkshopStatus.upcoming
    )
    workshops = db.exec(statement).all()
    if not workshops:
        raise HTTPException(status_code=404, detail="Nema aktivnih radionica.")
    return workshops

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




# --- POSTOJEĆA RUTA ZA PRIJAVU (Ažurirana na engleski) elma ---
@router.post("/registration", status_code=status.HTTP_201_CREATED)
def register_student(podaci: RegistrationCreate, db: Session = Depends(get_db)):
    # 1. Tražimo radionicu (pazimo na naziv modela Workshop)
    radionica = db.get(Workshop, podaci.workshop_id)
    
    if not radionica:
        raise HTTPException(status_code=404, detail="Workshop not found")

    # 2. Provjera kapaciteta
    if radionica.capacity <= 0:
        raise HTTPException(status_code=400, detail="No more seats available")

    # 3. Smanjujemo broj mjesta u radionici
    radionica.capacity -= 1 
    
    # 4. Kreiramo novu prijavu 
    # IZMJENA: Izbačen user_id=1 jer ga nema u Registration modelu
    nova_prijava = Registration(**podaci.model_dump()) 
    
    # 5. Spašavamo promjene u bazu
    db.add(radionica)
    db.add(nova_prijava)
    db.commit()
    db.refresh(nova_prijava)

    return {
        "status": "success",
        "message": "Registration successful!",
        "data": nova_prijava
    }

# --- NOVA RUTA ZA OTKAZIVANJE (GT1-22) --- elma
@router.delete("/cancellation/{registration_id}")
def cancel_registration(
    registration_id: int, 
    db: Session = Depends(get_db)
    # current_user: User = Depends(get_current_user) # Odkomentariši kad dodaš auth
):
    # 1. Pronađi prijavu u bazi koristeći novi naziv klase Registration
    prijava = db.get(Registration, registration_id)
    if not prijava:
        raise HTTPException(status_code=404, detail="Registration not found")

    # 2. Pronađi radionicu na koju se prijava odnosi
    radionica = db.get(Workshop, prijava.workshop_id)
    
    # 3. Oslobađanje mjesta
    if radionica:
        radionica.capacity += 1
        db.add(radionica)

    # 4. Obriši prijavu
    db.delete(prijava)
    db.commit()

    # 5. Poruka o uspješnoj odjavi
    return {"message": "Successfully unsubscribed. The spot is now free."}