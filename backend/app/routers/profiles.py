from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.profile import Profile, ProfileUpdate, ProfileResponse
from sqlmodel import select

router = APIRouter(prefix="/profiles", tags=["profiles"])

# -------------------------------------------------------
# Team 4 — Profiles & Dashboard
# This is your router. All your endpoints go here.
#
# Example protected endpoint:
#
# @router.get("/")
# def get_profile(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

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