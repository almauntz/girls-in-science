from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.profile import Profile, UpdateRoleRequest

router = APIRouter(prefix="/admin", tags=["admin-users"])


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
        profile_statement = select(Profile).where(Profile.user_id == user.id)
        profile = db.exec(profile_statement).first()
        extended_users.append({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "is_active": profile.is_active if profile else False
        })

    return extended_users


@router.put("/{user_id}/status")
def update_user_status(
    user_id: int,
    is_active: bool = Query(..., description="Postavite na true za aktiviranje, false za deaktiviranje"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_role_str = str(current_user.role).upper()
    if "ADMIN" not in user_role_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Samo administratori mogu mijenjati status korisnika."
        )

    statement = select(Profile).where(Profile.user_id == user_id)
    profile_to_update = db.exec(statement).first()

    if not profile_to_update:
        profile_to_update = Profile(user_id=user_id, is_active=is_active)
        db.add(profile_to_update)
    else:
        profile_to_update.is_active = is_active
        profile_to_update.deactivated_by = "admin" if not is_active else None
        db.add(profile_to_update)

    db.commit()
    db.refresh(profile_to_update)

    action_status = "aktivirana" if is_active else "deaktivirana"
    return {
        "message": f"Status korisnice je uspješno promijenjen na: {action_status}.",
        "user_id": user_id,
        "is_active": profile_to_update.is_active
    }


@router.put("/{user_id}/role")
def update_user_role(
    user_id: int,
    request_data: UpdateRoleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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
