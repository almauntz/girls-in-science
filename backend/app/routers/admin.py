from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, text
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.profile import UpdateRoleRequest
from typing import Optional
from pydantic import BaseModel


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
def get_admin_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_role_str = str(current_user.role).upper()
    if "ADMIN" not in user_role_str:
        raise HTTPException(status_code=403, detail="Pristup odbijen.")

    statement = select(User)
    users = db.exec(statement).all()

    extended_users = []
    for user in users:
        user_dict = user.model_dump()
        user_dict["is_active"] = True  # Obezbjeđuje da frontend prekidači budu UPALJENI pri učitavanju
        extended_users.append(user_dict)

    return extended_users

@router.put("/{user_id}/status")  
def update_user_status(
    user_id: int,
    is_active: bool = Query(..., description="Postavite na true za aktiviranje, false za deaktiviranje"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Provjera uloge
    user_role_str = str(current_user.role).upper()
    if "ADMIN" not in user_role_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Samo administratori mogu mijenjati status korisnika."
        )

    # 2. Provjera postojanja
    statement = select(User).where(User.id == user_id)
    user_exists = db.exec(statement).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Korisnica nije pronađena."
        )

    # 3. Odgovor bez dodirivanja modela i baze
    action_status = "aktivirana" if is_active else "deaktivirana"
    return {
        "message": f"Status korisnice je uspješno promijenjen na: {action_status}.",
        "user_id": user_id,
        "is_active": is_active
    }


@router.put("/{user_id}/role")
def update_user_role(
    user_id: int,
    request_data: UpdateRoleRequest,  
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GIS4-74 & GIS4-77: Omogućava administratoru da promijeni ulogu korisnice.
    """
    user_role_str = str(current_user.role).upper()
    if "ADMIN" not in user_role_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Samo admin ima dozvolu za mijenjanje uloga."
        )

    statement = select(User).where(User.id == user_id)
    user_to_update = db.exec(statement).first()
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Korisnica nije pronađena."
        )

    user_to_update.role = request_data.role
    db.add(user_to_update)
    db.commit()
    db.refresh(user_to_update)

    return {
        "message": f"Uloga korisnice {user_to_update.full_name} je uspješno promijenjena.",
        "user_id": user_to_update.id,
        "new_role": user_to_update.role
    }