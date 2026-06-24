from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.comment import Comment, CommentCreate, CommentRead
from app.models.news import NewsPost

router = APIRouter(prefix="/news", tags=["comments"])

@router.get("/{news_post_id}/comments", response_model=list[CommentRead])
def get_comments(news_post_id: int, db: Session = Depends(get_db)):
    news_post = db.get(NewsPost, news_post_id)
    if not news_post:
        raise HTTPException(status_code=404, detail="Objava nije pronađena")
    comments = db.exec(
        select(Comment).where(Comment.news_post_id == news_post_id)
    ).all()
    return comments

@router.post("/{news_post_id}/comments", response_model=CommentRead)
def create_comment(
    news_post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    news_post = db.get(NewsPost, news_post_id)
    if not news_post:
        raise HTTPException(status_code=404, detail="Objava nije pronađena")
    comment = Comment(
        content=data.content,
        user_id=current_user.id,
        news_post_id=news_post_id,
        user_full_name=current_user.full_name
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/{news_post_id}/comments/{comment_id}")
def delete_comment(
    news_post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen")
    if comment.news_post_id != news_post_id:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen")
    if current_user.role != UserRole.admin and comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nemate dozvolu za brisanje ovog komentara")
    db.delete(comment)
    db.commit()
    return {"message": "Komentar je uspješno obrisan"}