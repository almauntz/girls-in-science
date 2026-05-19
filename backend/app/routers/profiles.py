from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlmodel import Session, select, not_
from app.database import get_db
from app.core.security import get_current_user, verify_password, hash_password
from app.models.user import User, ChangePasswordRequest
from app.models.profile import Profile, ProfileUpdate, ProfileResponse, Workshop, WorkshopRegistration
from datetime import datetime
from typing import Dict, Any
import uuid
import os


router = APIRouter(prefix="/profiles", tags=["profiles"])


# Pomoćna funkcija — dohvat ili kreiranje profila
@router.get("/")
def profiles_placeholder():
    return {"message": "Profiles router is working — Team 4 builds here"}

def get_or_create_profile(user: User, db: Session) -> Profile:
    # Traži postojeći profil
    profile = db.exec(
        select(Profile).where(Profile.user_id == user.id)
    ).first()
    
    # Ako ne postoji — kreiraj ga
    if not profile:
        profile = Profile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return profile

@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = get_or_create_profile(current_user, db)
    
    return ProfileResponse(
        id=profile.id,
        user_id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        biography=profile.biography,
        field=profile.field,
        avatar=profile.avatar,
        role=current_user.role
    )

@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if profile_data.full_name is not None:
        if profile_data.full_name.strip() == "":
            raise HTTPException(status_code=400, detail="Ime ne smije biti prazno")
        current_user.full_name = profile_data.full_name
        db.add(current_user)

    profile = get_or_create_profile(current_user, db)
    if profile_data.biography is not None:
        profile.biography = profile_data.biography
    if profile_data.field is not None:
        profile.field = profile_data.field

    db.commit()
    db.refresh(current_user)
    db.refresh(profile)

    return ProfileResponse(
        id=profile.id,
        user_id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        biography=profile.biography,
        field=profile.field,
        avatar=profile.avatar,
        role=current_user.role
    )
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
            detail="Niste autorizovani."
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


@router.post("/dashboard/register", status_code=status.HTTP_201_CREATED)
def register_for_workshop(
    workshop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Omogućava trenutno ulogovanom korisniku da se prijavi na dostupnu radionicu.
    (GIS4-18: direktna prijava sa dashboarda)
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Niste autorizovani."
        )
    
    # Provjeravamo da li radionica postoji u bazi podataka
    workshop = db.get(Workshop, workshop_id)
    if not workshop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Radionica ne postoji."
        )
    # Provjeravamo da li je radionica već prošla
    if workshop.date < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ne možete se prijaviti na radionicu koja je već prošla."
        )
    # Provjeravamo da li je korisnik već prijavljen na ovu radionicu
    already_registered = db.exec(
        select(WorkshopRegistration).where(
            WorkshopRegistration.user_id == current_user.id,
            WorkshopRegistration.workshop_id == workshop_id
        )
    ).first()

    if already_registered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Već ste prijavljeni na ovu radionicu."
        )
    # Provjeravamo da li je radionica popunjena (ako radionica ima ograničen broj mjesta)
    # Brojimo koliko je trenutno prijavljenih korisnika na ovu radionicu
    current_registrations_count = len (
        db.exec(
            select(WorkshopRegistration).where(
                WorkshopRegistration.workshop_id == workshop_id
            )
        ).all()
    )

    if current_registrations_count >= workshop.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nažalost, sva mjesta za ovu radionicu su popunjena."
        )
    
    # Kreiranje nove prijave
    new_registration = WorkshopRegistration(
        user_id=current_user.id,
        workshop_id=workshop_id
    )
    db.add(new_registration)
    db.commit()
    return {"message": "Uspješno ste se prijavili na radionicu: {workshop.title}."}

# Endpoint za upload avatara
UPLOAD_DIR = "static/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

DOZVOLJENI_FORMATI = ["jpg", "jpeg", "png"]   
MAX_VELICINA = 2 * 1024 * 1024    

@router.post("/me/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)  # ← dodaj db parametar
):
    extension = file.filename.split(".")[-1].lower()
    if extension not in DOZVOLJENI_FORMATI:
        raise HTTPException(status_code=400, detail="Podržani formati su JPG i PNG.")
    
    sadrzaj = await file.read()
    if len(sadrzaj) > MAX_VELICINA:
        raise HTTPException(status_code=400, detail="Slika ne smije biti veća od 2MB.")

    filename = f"{uuid.uuid4()}.{extension}"
    file_path = f"{UPLOAD_DIR}/{filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(sadrzaj)

    url = f"/static/avatars/{filename}"

    profile = get_or_create_profile(current_user, db)
    profile.avatar = url
    db.add(profile)
    db.commit()

    return {"avatar_url": url}


@router.delete("/me/avatar", response_model=ProfileResponse)
def delete_avatar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Siguran i direktan endpoint za brisanje profilne slike.
    """
    # 1. Pronađi profil u bazi
    profile = db.exec(
        select(Profile).where(Profile.user_id == current_user.id)
    ).first()
    
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # 2. Fizičko brisanje fajla sa diska - SVE JE SADA UNUTAR JEDNOG SIGURNOG BLOKA
    if profile.avatar and str(profile.avatar).strip():
        file_path = str(profile.avatar).lstrip("/")
        
        # Tek ako putanja postoji i varijabla je stvorena, provjeravamo disk
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  

    # 3. Resetujemo avatar na None u bazi
    profile.avatar = None
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # 4. Slanje sigurnog odgovora bez NoneType zamki
    return ProfileResponse(
        id=profile.id if profile.id else 0,
        user_id=current_user.id,
        full_name=current_user.full_name if current_user.full_name else "Korisnik",
        email=current_user.email if current_user.email else "",
        biography=profile.biography,
        field=profile.field,
        avatar=None,
        role=current_user.role if current_user.role else "user"
    )

@router.patch("/me/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Stara lozinka nije tačna.")

    if data.new_password != data.confirm_new_password:
        raise HTTPException(status_code=400, detail="Nova lozinka i potvrda se ne poklapaju.")

    if len(data.new_password) < 8:
        raise HTTPException(status_code=400, detail="Nova lozinka mora imati najmanje 8 karaktera.")

    current_user.password_hash = hash_password(data.new_password)
    db.add(current_user)
    db.commit()

    return {"message": "Lozinka uspješno promijenjena."}