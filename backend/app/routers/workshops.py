from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import Optional

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.workshops_models import (RegistrationRead, Workshop,RegistrationCreate,Registration, WorkshopStatus, WorkshopCreate,
                                          WorkshopUpdate, WorkshopRead, WorkshopList,WorkshopDetailRead, WorkshopProposal,
                                            ProposalCreate, ProposalRead, ProposalUserRead, ProposalApprove, ProposalReject, ProposalStatus,WaitingList, UserNotification,WorkshopRating, RatingCreate, RatingRead)
from sqlalchemy import func
from sqlalchemy.orm import Session

router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.get("/my-promotion")
def my_promotion(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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

    workshop = db.query(Workshop).filter(
        Workshop.ID_workshop == registration.workshop_id
    ).first()

    return {
        "promotion": {
            "user_id": current_user.id,
            "workshop_id": registration.workshop_id,
            "workshop_title": workshop.title if workshop else "Radionica",
            "status": registration.status,
            "is_promoted": registration.was_promoted
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
                phone="",
                was_promoted=True
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
    #izmjena na prikazu radionica - dodan upit za radionice koje su upcoming  i completed
    statement = select(Workshop).where(    
        Workshop.status.in_([WorkshopStatus.upcoming, WorkshopStatus.completed])
    )
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
# Za  automatsko ažuriranje statusa radionica nakon isteka vremena
@router.post("/auto-complete", status_code=200)
def auto_complete_workshops(db: Session = Depends(get_db)):
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    
    workshops = db.execute(
        select(Workshop).where(
            Workshop.status == WorkshopStatus.upcoming,
            Workshop.end_time < now
        )
    ).scalars().all()

    updated = 0
    for w in workshops:
        w.status = WorkshopStatus.completed
        db.add(w)
        updated += 1

    db.commit()
    return {"message": f"{updated} radionica označeno kao završeno."}



def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Samo administrator može izvršiti ovu akciju."
        )
    return current_user
   

@router.get("/admin", response_model=list[ProposalRead])
def get_admin_panel(
    status_filter: Optional[ProposalStatus] =  Query(default=None),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    statement = select(WorkshopProposal).order_by(WorkshopProposal.created_at.desc())
    if status_filter:
        statement = statement.where(WorkshopProposal.status == status_filter)
    return db.execute(statement).scalars().all()


@router.get("/proposals/my", response_model=list[ProposalUserRead])
def get_my_proposals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = (
        select(WorkshopProposal)
        .where(WorkshopProposal.proposed_by_id == current_user.id)
        .order_by(WorkshopProposal.created_at.desc())
    )
    return db.execute(statement).scalars().all()


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
        created_by_id=admin.id,
        organizer_name=data.organizer_name,
        organizer_email=data.organizer_email,
        organizer_phone=data.organizer_phone
    )
    db.add(workshop)
    db.commit()
    db.refresh(workshop)
    try:
        svi_korisnici = db.execute(select(User)).scalars().all()
        for korisnik in svi_korisnici:
            nova_notifikacija = UserNotification(
                user_id=korisnik.id,
                title="Nova radionica je dostupna! 🎉",
                body=f"Objavljena je radionica: '{workshop.title}'. Prijavite se na vrijeme!"
            )
            db.add(nova_notifikacija)
        db.commit()
        print("✅ Notifikacije uspješno spremljene u bazu!")
    except Exception as e:
        print(f"🚨 Greška pri kreiranju notifikacija: {e}")
    return workshop

@router.get("/unread-notifications")
def get_unread_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        statement = select(UserNotification).where(
            UserNotification.user_id == current_user.id,
            UserNotification.is_read == False
        )
        notifications = db.execute(statement).scalars().all()
        
        result = [
            {"id": n.id, "title": n.title, "body": n.body} 
            for n in notifications
        ]
        
        for n in notifications:
            n.is_read = True
            db.add(n)
            
        if notifications:
            db.commit()
            
        return result
    except Exception as e:
        print(f"🚨 GREŠKA U NOTIFIKACIJAMA: {e}")
        return []
# =============================================================

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

# -- Proposal user endpoints -------------------------------------------------------

@router.get("/proposals/{proposal_id}", response_model=ProposalRead)
def get_proposal_detail(
    proposal_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    proposal = db.get(WorkshopProposal, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Prijedlog nije pronađen.")
    return proposal


@router.patch("/proposals/{proposal_id}/approve", response_model=ProposalRead)
def approve_proposal(
    proposal_id: int,
    data: ProposalApprove,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    proposal = db.get(WorkshopProposal, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Prijedlog nije pronađen.")
    if proposal.status != ProposalStatus.pending:
        raise HTTPException(status_code=400, detail=f"Prijedlog je već obrađen (status: {proposal.status}).")

    proposal.status = ProposalStatus.accepted
    proposal.admin_note = data.admin_note

    if data.create_workshop:
        missing = [f for f, v in {
            "location": data.location,
            "date": data.date,
            "end_time": data.end_time,
            "capacity": data.capacity
        }.items() if v is None]
        if missing:
            raise HTTPException(
                status_code=422,
                detail=f"Za kreiranje radionice nedostaju: {', '.join(missing)}"
            )
        workshop = Workshop(
            title=proposal.title,
            description=proposal.description,
            location=data.location,
            date=data.date,
            end_time=data.end_time,
            capacity=data.capacity,
            created_by_id=admin.id,
            status=WorkshopStatus.upcoming,
        )
        db.add(workshop)

    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal


@router.post("/proposals", response_model=ProposalUserRead, status_code=status.HTTP_201_CREATED)
def submit_proposal(
    data: ProposalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    proposal = WorkshopProposal(
        title=data.title,
        description=data.description,
        proposed_by_id=current_user.id,
        proposed_by_email=current_user.email,
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal


@router.patch("/proposals/{proposal_id}/reject", response_model=ProposalRead)
def reject_proposal(
    proposal_id: int,
    data: ProposalReject,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    proposal = db.get(WorkshopProposal, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Prijedlog nije pronađen.")
    if proposal.status != ProposalStatus.pending:
        raise HTTPException(status_code=400, detail=f"Prijedlog je već obrađen (status: {proposal.status}).")

    proposal.status = ProposalStatus.rejected
    proposal.admin_note = data.admin_note

    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal



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
        organizer_name=workshop.organizer_name,
        organizer_email=workshop.organizer_email,
        organizer_phone=workshop.organizer_phone,
        free_spots=free_spots
    )

@router.get("/{workshop_id}/registrations", response_model=list[RegistrationRead])
def get_workshop_registrations(
    workshop_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    workshop = db.get(Workshop, workshop_id)
    if not workshop:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena.")
 
    registrations = db.execute(
        select(Registration).where(Registration.workshop_id == workshop_id)
    ).scalars().all()
 
    return registrations

#Rating endpoints -------------------------------------------------------

@router.post("/{workshop_id}/ratings", response_model=RatingRead, status_code=status.HTTP_201_CREATED)
def create_rating(
    workshop_id: int,
    data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Postoji li radionica?
    workshop = db.get(Workshop, workshop_id)
    if not workshop:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena.")

    # 2. Je li radionica završena?
    if workshop.status != WorkshopStatus.completed:
        raise HTTPException(status_code=400, detail="Radionica još nije završena.")

    # 3. Je li korisnica bila registrovana?
    registration = db.execute(
        select(Registration).where(
            Registration.workshop_id == workshop_id,
            Registration.user_id == current_user.id
        )
    ).scalars().first()

    if not registration:
        raise HTTPException(status_code=403, detail="Niste bili prijavljeni na ovu radionicu.")

    # 4. Je li već ostavila ocjenu?
    existing = db.execute(
        select(WorkshopRating).where(
            WorkshopRating.registration_id == registration.id
        )
    ).scalars().first()

    if existing:
        if existing:
          raise HTTPException(status_code=409, detail="Već ste ocjenili ovu radionicu.")
    new_rating = WorkshopRating(
        registration_id=registration.id,
        user_id=current_user.id,
        workshop_id=workshop_id,
        score=data.score,
        comment=data.comment
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating


@router.get("/{workshop_id}/ratings", response_model=list[RatingRead])
def get_ratings(workshop_id: int, db: Session = Depends(get_db)):
    workshop = db.get(Workshop, workshop_id)
    if not workshop:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena.")

    return db.execute(
        select(WorkshopRating).where(WorkshopRating.workshop_id == workshop_id)
        .order_by(WorkshopRating.created_at.desc())
    ).scalars().all()


@router.get("/{workshop_id}/ratings/average")
def get_ratings_average(workshop_id: int, db: Session = Depends(get_db)):
    workshop = db.get(Workshop, workshop_id)
    if not workshop:
        raise HTTPException(status_code=404, detail="Radionica nije pronađena.")

    row = db.execute(
        select(func.avg(WorkshopRating.score), func.count(WorkshopRating.id))
        .where(WorkshopRating.workshop_id == workshop_id)
    ).first()

    avg = float(row[0]) if row and row[0] is not None else 0.0
    count = int(row[1]) if row and row[1] is not None else 0

    return {"average": round(avg, 2), "count": count}