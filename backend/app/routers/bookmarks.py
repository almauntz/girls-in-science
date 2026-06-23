from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.bookmark import Bookmark
from app.models.role_model import RoleModel

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])

@router.post("/{role_model_id}")
def add_bookmark(
    role_model_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role_model = db.get(RoleModel, role_model_id)
    if not role_model:
        raise HTTPException(status_code=404, detail="Profil nije pronađen")
    
    existing = db.exec(
        select(Bookmark).where(
            Bookmark.user_id == current_user.id,
            Bookmark.role_model_id == role_model_id
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Profil je već dodan u favorite")
    
    bookmark = Bookmark(user_id=current_user.id, role_model_id=role_model_id)
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return {"message": "Profil dodan u favorite"}

@router.delete("/{role_model_id}")
def remove_bookmark(
    role_model_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookmark = db.exec(
        select(Bookmark).where(
            Bookmark.user_id == current_user.id,
            Bookmark.role_model_id == role_model_id
        )
    ).first()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark nije pronađen")
    
    db.delete(bookmark)
    db.commit()
    return {"message": "Profil uklonjen iz favorita"}

@router.get("/")
def get_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookmarks = db.exec(
        select(Bookmark).where(Bookmark.user_id == current_user.id)
    ).all()
    
    role_models = []
    for bookmark in bookmarks:
        role_model = db.get(RoleModel, bookmark.role_model_id)
        if role_model:
            role_models.append(role_model)
    
    return role_models