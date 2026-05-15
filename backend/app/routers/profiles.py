from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, not_
from datetime import datetime
from typing import Dict, Any

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.profile import Workshop, WorkshopRegistration

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/dashboard", response_model=Dict[str, Any])
def get_personal_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Dohvata personalizovani dashboard za trenutno ulogovanog korisnika.
    Vraća tri sekcije: Moje radionice, Nove radionice i Dostupne radionice.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Niste autorizovani"
        )
    user_id = current_user.id

    # 1. Moje radionice - Radionice na koje je korisnik prijavljen
    # Radimo JOIN između Workshop i WorkshopRegistration da dobijemo radionice na koje je trenutni korisnik prijavljen
    my_workshops_query = (
        select(Workshop)
        .join(WorkshopRegistration)
        .where(WorkshopRegistration.user_id == user_id)
        .order_by(Workshop.date.asc()) 
    )
    my_workshops = db.exec(my_workshops_query).all()

    # Izvlačimo samo ID-eve mojih radionica da bismo ih lakše filtrirali u "Dostupne radionice"
    my_workshop_ids = [w.id for w in my_workshops]

    # 2. SEKCIJA: Nove radionice (posljednje 3 dodane u sistem a da im datum nije prošao)
    new_workshops_query = (
        select(Workshop)
        .where(Workshop.date >= datetime.utcnow())  # Samo buduće radionice
        .order_by(Workshop.created_at.desc())  # Najnovije prvo
        .limit(3)  # Ograničavamo na 3 najnovije
    )
    new_workshops = db.exec(new_workshops_query).all()

    # 3. SEKCIJA: Dostupne radionice (sve buduće radionice na koje korisnik nije prijavljen)
    # Koristimo not_(Workshop.id.in_(my_workshop_ids)) da izuzmemo radionice na koje je korisnik već prijavljen
    if my_workshop_ids:
        available_workshops_query = (
            select(Workshop)
            .where(
                Workshop.date >= datetime.utcnow(),  # Samo buduće radionice
                not_(Workshop.id.in_(my_workshop_ids))  # Izuzimamo moje radionice
            )
            .order_by(Workshop.date.asc())  # Najbliže prvo
        )
    else: 
        # Ako korisnik nije prijavljen ni na jednu radionicu, prikazujemo sve buduće radionice
        available_workshops_query = (
            select(Workshop)
            .where(Workshop.date >= datetime.utcnow())  # Samo buduće radionice
            .order_by(Workshop.date.asc())  # Najbliže prvo
        )
    available_workshops = db.exec(available_workshops_query).all()

    # Pakujemo sve u jedan jasan JSON odgovor za Vue frontend
    return {
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "role": current_user.role
        },
        "my_workshops": my_workshops,
        "new_workshops": new_workshops,
        "available_workshops": available_workshops
    }