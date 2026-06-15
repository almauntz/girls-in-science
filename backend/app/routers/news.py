from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/news", tags=["news"])

# -------------------------------------------------------
# Team 4 — News & Blog
# This is your router. All your endpoints go here.
#
# News posts are stories, articles, and updates from the centre.
# A news post can optionally reference a RoleModel — coordinate
# with Team 3 on the RoleModel model and its ID field.
#
# Your team will define the NewsPost model in app/models/news.py
#
# Example protected endpoint:
#
# @router.get("/")
# def get_news(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": "your code here"}
#
# -------------------------------------------------------

@router.get("/")
def news_placeholder():
    return {"message": "News router is working — Team 4 builds here"}
