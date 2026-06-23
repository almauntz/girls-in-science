from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.role_model import RoleModel, RoleModelCreate, RoleModelUpdate
from fastapi import UploadFile, File
import shutil
import os

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

@router.patch("/{id}")
def update_role_model(id: int, data: RoleModelUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Samo administratorica može uređivati profile")
    role_model = db.get(RoleModel, id)
    if not role_model:
        raise HTTPException(status_code=404, detail="Profil nije pronađen")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(role_model, key, value)
    db.add(role_model)
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

@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Samo administratorica može uploadovati slike")
    upload_dir = "uploads/rolemodels"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "image_url": f"/uploads/rolemodels/{file.filename}"
    }