from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.role_model import RoleModel, RoleModelCreate

router = APIRouter(prefix="/role-models", tags=["role_models"])

@router.get("/")
def get_role_models(db: Session = Depends(get_db)):
    statement = select(RoleModel).order_by(RoleModel.last_name, RoleModel.first_name)
    role_models = db.exec(statement).all()
    return role_models

@router.get("/{id}")
def get_role_model(id: int, db: Session = Depends(get_db)):
    role_model = db.get(RoleModel, id)
    if not role_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profil nije pronađen")
    return role_model

@router.put("/{id}")
def update_role_model(id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Samo administratorica može uređivati profile")
    role_model = db.get(RoleModel, id)
    if not role_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profil nije pronađen")
    allowed_fields = {"first_name", "last_name", "stem_field", "institution", "position", "biography", "achievements"}
    for key, value in data.items():
        if key in allowed_fields:
            setattr(role_model, key, value)
    db.commit()
    db.refresh(role_model)
    return role_model

@router.post("/")
def create_role_model(role_model_data: RoleModelCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Samo administratorica može dodavati profile")
    role_model = RoleModel(**role_model_data.model_dump())
    db.add(role_model)
    db.commit()
    db.refresh(role_model)
    return role_model

@router.delete("/{role_model_id}")
def delete_role_model(
    role_model_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Samo administratorica može brisati profile")
    
    role_model = db.get(RoleModel, role_model_id)
    if not role_model:
        raise HTTPException(status_code=404, detail="Profil nije pronađen")
    
    db.delete(role_model)
    db.commit()
    return {"message": "Profil je uspješno obrisan"}
