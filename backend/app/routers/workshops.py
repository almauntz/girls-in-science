from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.workshops_models import Workshop,RegistrationCreate,Registration, WorkshopStatus, WorkshopCreate, WorkshopUpdate, WorkshopRead, WorkshopList,WorkshopDetailRead, WaitingList,RegistrationStatus
from datetime import datetime, timezone
from sqlalchemy import func,select
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlmodel import select
router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.get("/my-promotion")
def my_promotion(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # uzmi zadnju VALID registraciju (ne cancelled)
    registration = (
        db.query(Registration)
        .filter(
            Registration.user_id == current_user.id,
            Registration.status.in_(["registered", "waiting"])
        )
        .order_by(Registration.created_at.desc())
        .first()
    )

    if not registration:
        return {"promotion": None}

    # provjeri da li je user bio "promoted"
    is_promoted = registration.status == "registered"

    return {
        "promotion": {
            "user_id": current_user.id,
            "workshop_id": registration.workshop_id,
            "status": registration.status,
            "is_promoted": is_promoted
        }
    }








@router.delete("/cancellation/{workshop_id}")
def cancel_registration(
    workshop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. pronađi registraciju korisnika
    statement = select(Registration).where(
        Registration.workshop_id == workshop_id,
        Registration.user_id == current_user.id
    )

    registration = db.execute(statement).scalars().first()

    if not registration:
        raise HTTPException(
            status_code=404,
            detail="Nije pronađena vaša prijava za ovu radionicu."
        )

    # 2. obriši registraciju
    db.delete(registration)
    db.commit()

    # 3. NAĐI PRVOG NA WAITLISTI (FIFO)
    waiting_statement = select(WaitingList).where(
        WaitingList.workshop_id == workshop_id
    ).order_by(WaitingList.created_at.asc())

    waiting_user = db.execute(waiting_statement).scalars().first()

    promoted_user_id = None

    # 4. PROMOTE
    if waiting_user:
        user = db.get(User, waiting_user.user_id)

        if user:
            new_registration = Registration(
                user_id=user.id,
                workshop_id=workshop_id,
                status="registered",
                first_name=user.full_name,
                last_name="",
                email=user.email,
                phone=""
            )

            db.add(new_registration)
            db.delete(waiting_user)
            db.commit()

            promoted_user_id = user.id

    # 5. RESPONSE
    return {
        "message": "Uspješno ste odustali od radionice.",
        "promoted_user_id": promoted_user_id
    }




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

    # broj prijava
    broj_prijava = db.execute(
        select(func.count(Registration.id)).where(
            Registration.workshop_id == podaci.workshop_id
        )
    ).scalar() or 0

    if broj_prijava >= radionica.capacity:
        raise HTTPException(status_code=400, detail="Nažalost, sva mjesta su popunjena!")

    #DUPLA PROVJERA: EMAIL
    postojeca_email = db.execute(
        select(Registration).where(
            Registration.workshop_id == podaci.workshop_id,
            func.lower(Registration.email) == podaci.email.lower().strip()
        )
    ).scalars().first()

    if postojeca_email:
        raise HTTPException(status_code=400, detail="Ovaj email već je registrovan!")

    # DUPLA PROVJERA: USER_ID
    postojeca_user = db.execute(
        select(Registration).where(
            Registration.workshop_id == podaci.workshop_id,
            Registration.user_id == current_user.id
        )
    ).scalars().first()

    if postojeca_user:
        raise HTTPException(status_code=400, detail="Već ste prijavljeni (user)!")


    # kreiranje prijave
    nova_prijava = Registration(
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


@router.get("/registration/check/{workshop_id}")
def check_registration(
    workshop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    exists = db.execute(
        select(Registration).where(
            Registration.workshop_id == workshop_id,
            Registration.user_id == current_user.id
        )
    ).scalars().first()

    return {
        "registered": exists is not None
    }


##LISTA ČEKANJA - WAITING LIST ------------------------------------------------------- MAHIR

@router.post("/waiting-list/join/{workshop_id}")
def join_waiting_list(
    workshop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Provjera da li je korisnik već PRIJAVLJEN
    existing_registration = db.execute(
        select(Registration).where(
            Registration.workshop_id == workshop_id,
            Registration.user_id == current_user.id,
            Registration.status == "registered"
        )
    ).scalars().first()

    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Već ste prijavljeni na ovu radionicu."
        )

    # 2. Provjera da li je već na WAITING LISTI
    existing_waiting = db.execute(
        select(WaitingList).where(
            WaitingList.workshop_id == workshop_id,
            WaitingList.user_id == current_user.id
        )
    ).first()

    if existing_waiting:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Već ste na listi čekanja."
        )

    # 3. Dodavanje na kraj reda (FIFO)
    waiting_entry = WaitingList(
        workshop_id=workshop_id,
        user_id=current_user.id
    )

    db.add(waiting_entry)
    db.commit()
    db.refresh(waiting_entry)

    # 4. Izračun pozicije u redu
    position = db.execute(
        select(WaitingList)
        .where(WaitingList.workshop_id == workshop_id)
        .order_by(WaitingList.created_at)
    ).scalars().all()

    position_index = [w.id for w in position].index(waiting_entry.id) + 1

    return {
        "message": "Uspješno ste dodani na listu čekanja.",
        "position": position_index,
        "total_in_queue": len(position)
    }


@router.get("/waiting-list/status/{workshop_id}")
def waiting_list_status(
    workshop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.execute(
        select(WaitingList).where(
            WaitingList.workshop_id == workshop_id,
            WaitingList.user_id == current_user.id
        )
    ).scalars().first()

    if not entry:
        return {"on_waiting_list": False}

    queue = db.execute(
        select(WaitingList)
        .where(WaitingList.workshop_id == workshop_id)
        .order_by(WaitingList.created_at)
    ).scalars().all()

    position = [w.id for w in queue].index(entry.id) + 1

    return {
        "on_waiting_list": True,
        "position": position
    }


@router.get("/my-promotion")
def my_promotion(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # uzmi zadnju VALID registraciju (ne cancelled)
    registration = (
        db.query(Registration)
        .filter(
            Registration.user_id == current_user.id,
            Registration.status.in_(["registered", "waiting"])
        )
        .order_by(Registration.created_at.desc())
        .first()
    )

    if not registration:
        return {"promotion": None}

    # provjeri da li je user bio "promoted"
    is_promoted = registration.status == "registered"

    return {
        "promotion": {
            "user_id": current_user.id,
            "workshop_id": registration.workshop_id,
            "status": registration.status,
            "is_promoted": is_promoted
        }
    }