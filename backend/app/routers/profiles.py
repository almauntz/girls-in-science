from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Body, Request
from sqlmodel import Session, select, not_
from sqlalchemy import func
from app.database import get_db
from app.core.security import get_current_user, verify_password, hash_password, create_access_token,decode_access_token
from app.models.user import User, UserRole
from app.models.profile import Profile, ProfileUpdate, ProfileResponse, ChangePasswordRequest, PublicProfileResponse
from app.models.workshops_models import Workshop, Registration as WorkshopRegistration
from datetime import datetime
from typing import Dict, Any
import uuid
import os
from typing import Optional
import json


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/")
def get_all_profiles(db: Session = Depends(get_db)):
    try:
        # Pokušavamo prvo povući sve korisnike iz User tabele
        statement = select(User)
        users = db.exec(statement).all()
        return users
    except Exception as e:
        print(f"BACKEND GREŠKA: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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


def parse_profile_json_fields(profile: Profile) -> dict:
    """Parsira JSON stringove iz baze u Python liste."""
    def safe_parse(val):
        if not val:
            return []
        try:
            return json.loads(val)
        except Exception:
            return []

    return {
        "languages": safe_parse(profile.languages),
        "experience": safe_parse(profile.experience),
        "education": safe_parse(profile.education),
        "skills": safe_parse(profile.skills),
    }

@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = get_or_create_profile(current_user, db)
    
    parsed = parse_profile_json_fields(profile)
    return ProfileResponse(
        id=profile.id,
        user_id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        biography=profile.biography,
        field=profile.field,
        avatar=profile.avatar,
        role=current_user.role,
        location=profile.location,
        show_biography=profile.show_biography,
        show_field=profile.show_field,
        show_location=profile.show_location,
        languages=parsed["languages"],
        experience=parsed["experience"],
        education=parsed["education"],
        skills=parsed["skills"],
        linkedin_url=profile.linkedin_url,
        github_url=profile.github_url,
        twitter_url=profile.twitter_url,
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
    if profile_data.location is not None:
        profile.location = profile_data.location
    if profile_data.email is not None:
        current_user.email = profile_data.email
    
       # Privacy polja
    if profile_data.show_biography is not None:
        profile.show_biography = profile_data.show_biography
    if profile_data.show_field is not None:
        profile.show_field = profile_data.show_field
    if profile_data.show_location is not None:
        profile.show_location = profile_data.show_location

    if profile_data.languages is not None:
        profile.languages = json.dumps([l.dict() for l in profile_data.languages])
    if profile_data.experience is not None:
        profile.experience = json.dumps([e.dict() for e in profile_data.experience])
    if profile_data.education is not None:
        profile.education = json.dumps([e.dict() for e in profile_data.education])
    if profile_data.skills is not None:
        profile.skills = json.dumps(profile_data.skills)
    if profile_data.linkedin_url is not None:
        profile.linkedin_url = profile_data.linkedin_url
    if profile_data.github_url is not None:
        profile.github_url = profile_data.github_url
    if profile_data.twitter_url is not None:
        profile.twitter_url = profile_data.twitter_url

    db.commit()
    db.refresh(current_user)
    db.refresh(profile)

    parsed=parse_profile_json_fields(profile)
    return ProfileResponse(
        id=profile.id,
        user_id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        biography=profile.biography,
        field=profile.field,
        avatar=profile.avatar,
        role=current_user.role,
        location=profile.location,
        show_biography=profile.show_biography,
        show_field=profile.show_field,
        show_location=profile.show_location,
        languages=parsed["languages"],
        experience=parsed["experience"],
        education=parsed["education"],
        skills=parsed["skills"],
        linkedin_url=profile.linkedin_url,
        github_url=profile.github_url,
        twitter_url=profile.twitter_url,
    )

@router.get("/dashboard", response_model=Dict[str, Any])
def get_personal_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id

    # IDs of workshops the user is registered for
    my_registration_workshop_ids = [
        r.workshop_id for r in db.exec(
            select(WorkshopRegistration).where(WorkshopRegistration.user_id == user_id)
        ).all()
    ]

    # My workshops
    if my_registration_workshop_ids:
        my_workshops = db.exec(
            select(Workshop)
            .where(Workshop.ID_workshop.in_(my_registration_workshop_ids))
            .order_by(Workshop.date.asc())
        ).all()
    else:
        my_workshops = []

    # New workshops (latest 3 upcoming)
    new_workshops = db.exec(
        select(Workshop)
        .where(Workshop.date >= datetime.utcnow())
        .order_by(Workshop.created_at.desc())
        .limit(3)
    ).all()

    # Available workshops (upcoming, not already registered)
    if my_registration_workshop_ids:
        available_workshops = db.exec(
            select(Workshop)
            .where(
                Workshop.date >= datetime.utcnow(),
                not_(Workshop.ID_workshop.in_(my_registration_workshop_ids))
            )
            .order_by(Workshop.date.asc())
        ).all()
    else:
        available_workshops = db.exec(
            select(Workshop)
            .where(Workshop.date >= datetime.utcnow())
            .order_by(Workshop.date.asc())
        ).all()

    def workshop_to_dict(w):
        return {
            "id": w.ID_workshop,
            "title": w.title,
            "description": w.description,
            "date": w.date.isoformat() if w.date else None,
            "capacity": w.capacity,
            "created_at": w.created_at.isoformat() if w.created_at else None,
        }

    return {
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "role": current_user.role
        },
        "my_workshops": [workshop_to_dict(w) for w in my_workshops],
        "new_workshops": [workshop_to_dict(w) for w in new_workshops],
        "available_workshops": [workshop_to_dict(w) for w in available_workshops],
    }


@router.post("/dashboard/register", status_code=status.HTTP_201_CREATED)
def register_for_workshop(
    workshop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workshop = db.exec(select(Workshop).where(Workshop.ID_workshop == workshop_id)).first()
    if not workshop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Radionica ne postoji.")

    if workshop.date < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ne možete se prijaviti na radionicu koja je već prošla.")

    already_registered = db.exec(
        select(WorkshopRegistration).where(
            WorkshopRegistration.user_id == current_user.id,
            WorkshopRegistration.workshop_id == workshop_id
        )
    ).first()
    if already_registered:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Već ste prijavljeni na ovu radionicu.")

    current_count = len(db.exec(
        select(WorkshopRegistration).where(WorkshopRegistration.workshop_id == workshop_id)
    ).all())
    if current_count >= workshop.capacity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nažalost, sva mjesta su popunjena.")

    new_registration = WorkshopRegistration(
        user_id=current_user.id,
        workshop_id=workshop_id
    )
    db.add(new_registration)
    db.commit()
    return {"message": f"Uspješno ste se prijavili na radionicu: {workshop.title}."}

# Endpoint za upload avatara
UPLOAD_DIR = "static/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]   
MAX_FILE_SIZE = 2 * 1024 * 1024    

@router.post("/me/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)  # ← dodaj db parametar
):
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Podržani formati su JPG, JPEG i PNG.")
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Slika ne smije biti veća od 2MB.")

    filename = f"{uuid.uuid4()}.{extension}"
    file_path = f"{UPLOAD_DIR}/{filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(content)

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

# PATCH /profiles/me/deactivate
@router.patch("/me/deactivate", status_code=200)
def deactivate_my_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = get_or_create_profile(current_user, db)
    profile.deactivated_by = "user"
    profile.is_active = False
    db.add(profile)
    db.commit()

    return {"message": "Vaš nalog je uspješno deaktiviran."}

@router.post("/login-check", status_code=200)
def login_check(
    email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    user = db.exec(select(User).where(User.email == email)).first()
    
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Neispravni kredencijali.")
    
    profile = db.exec(select(Profile).where(Profile.user_id == user.id)).first()
    
    if profile and not profile.is_active:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Vaš nalog je deaktiviran. Želite li ga reaktivirati?",
                "reactivatable": True
            }
        )
    
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me/history", response_model=list[Workshop])
def get_my_workshop_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.exec(
        select(Workshop)
        .join(WorkshopRegistration, WorkshopRegistration.workshop_id == Workshop.ID_workshop)
        .where(
            WorkshopRegistration.user_id == current_user.id,
            func.coalesce(Workshop.end_time, Workshop.date) < datetime.utcnow()
        )
        .order_by(Workshop.date.desc())
    ).all()
    return history


@router.post("/reactivate", status_code=200)
def reactivate_account(
    email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    user = db.exec(select(User).where(User.email == email)).first()
    
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Neispravni kredencijali.")
    
    profile = db.exec(select(Profile).where(Profile.user_id == user.id)).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profil nije pronađen.")
    
    profile.is_active = True
    db.add(profile)
    db.commit()

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/{user_id}", response_model=PublicProfileResponse)
def get_public_profile(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnica nije pronađena.")
    
    profile = db.exec(
        select(Profile).where(Profile.user_id == user_id)
    ).first()

    if profile and not profile.is_active:
        raise HTTPException(status_code=404, detail="Korisnica nije pronađena.")

    # Čitaj token iz Authorization headera
    email = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = decode_access_token(token)
        if payload is not None:
            email = user.email

    parsed=parse_profile_json_fields(profile) if profile else {}
    return PublicProfileResponse(
        full_name=user.full_name,
        field=profile.field if (profile and profile.show_field) else None,
        biography=profile.biography if (profile and profile.show_biography) else None,
        avatar=profile.avatar if profile else None,
        email=email,
        location=profile.location if (profile and profile.show_location) else None,
        languages=parsed.get("languages", []),
        experience=parsed.get("experience", []),
        education=parsed.get("education", []),
        skills=parsed.get("skills", []),
        linkedin_url=profile.linkedin_url if profile else None,
        github_url=profile.github_url if profile else None,
        twitter_url=profile.twitter_url if profile else None
    )