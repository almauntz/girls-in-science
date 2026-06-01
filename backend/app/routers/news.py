from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.models.role_model import RoleModel
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.news import NewsPost, NewsPostCreate, NewsPostUpdate

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/{id}")
def get_news_post(id: int, db: Session = Depends(get_db)):
    news_post = db.get(NewsPost, id)
    if not news_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objava nije pronađena")
    _ = news_post.role_models
    return news_post

@router.post("/")
def create_news_post(
    news_data: NewsPostCreate,
    db: Session = Depends(get_db)
):
    if not news_data.title or not news_data.content:

        raise HTTPException(
            status_code=400,
            detail="Title i content su obavezni"
        )

    news_post = NewsPost(
        title=news_data.title,
        content=news_data.content,
        author=news_data.author,
        image_url=news_data.image_url
    )

    if news_data.role_model_ids:

        role_models = []

        for role_model_id in news_data.role_model_ids:

            role_model = db.get(RoleModel, role_model_id)

            if role_model:
                role_models.append(role_model)

        news_post.role_models = role_models

    db.add(news_post)

    db.commit()

    db.refresh(news_post)

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

@router.patch("/{id}")
def update_news_post(
    id: int,
    data: NewsPostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Samo administratorica može uređivati objave")
    news_post = db.get(NewsPost, id)
    if not news_post:
        raise HTTPException(status_code=404, detail="Objava nije pronađena")
    update_data = data.model_dump(exclude_unset=True, exclude={"role_model_ids"})
    for key, value in update_data.items():
        setattr(news_post, key, value)
    if data.role_model_ids is not None:
        role_models = []
        for role_model_id in data.role_model_ids:
            role_model = db.get(RoleModel, role_model_id)
            if role_model:
                role_models.append(role_model)
        news_post.role_models = role_models
    db.add(news_post)
    db.commit()
    db.refresh(news_post)
    _ = news_post.role_models
    return news_post