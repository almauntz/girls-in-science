from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.role_model import RoleModel, RoleModelCreate


router = APIRouter(prefix="/role-models", tags=["role_models"])

# -------------------------------------------------------
# Team 3 — Role Models
# This is your router. All your endpoints go here.
#
# Role models are inspiring women in STEM. Build a directory
# that lets users browse and search them.
#
# Your team will define the RoleModel model in app/models/role_model.py
# Coordinate with the News team — a NewsPost can reference a RoleModel.
#
# Example protected endpoint:
#
# @router.get("/")
# def get_role_models(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

@router.get("/")
def role_models_placeholder():
    return {"message": "Role Models router is working — Team 3 builds here"}


@router.post("/")
def create_role_model(
    role_model_data: RoleModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Samo administratorica može dodavati profile")
    
    role_model = RoleModel(**role_model_data.model_dump())
    db.add(role_model)
    db.commit()
    db.refresh(role_model)
    return role_model