from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_db
from app.models.news import NewsPost

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/{id}")
def get_news_post(id: int, db: Session = Depends(get_db)):
    news_post = db.get(NewsPost, id)
    if not news_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objava nije pronađena")
    return news_post