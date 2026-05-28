from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.news import NewsPost

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/{id}")
def get_news_post(id: int, db: Session = Depends(get_db)):
    news_post = db.get(NewsPost, id)
    if not news_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objava nije pronađena")
    _ = news_post.role_models
    return news_post

@router.get("/")
def get_news_posts(db: Session = Depends(get_db)):
    statement = select(NewsPost).order_by(NewsPost.created_at.desc())
    news_posts = db.exec(statement).all()
    return news_posts

@router.delete("/{id}")
def delete_news_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Samo administratorica može brisati objave")
    news_post = db.get(NewsPost, id)
    if not news_post:
        raise HTTPException(status_code=404, detail="Objava nije pronađena")
    db.delete(news_post)
    db.commit()
    return {"message": "Objava je uspješno obrisana"}