from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.role_model import RoleModel

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
def get_role_models(
    db: Session=Depends(get_db)
):
    statement=select(RoleModel).order_by(
        RoleModel.last_name,
        RoleModel.first_name
    )
    role_models=db.exec(statement).all()
    return role_models