from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Text
from sqlalchemy.sql import func


class NewsPostRoleModelLink(SQLModel, table=True):
    __tablename__ = "news_post_role_model_links"
    news_post_id: Optional[int] = Field(default=None, foreign_key="news_posts.id", primary_key=True)
    role_model_id: Optional[int] = Field(default=None, foreign_key="role_models.id", primary_key=True)


class NewsPost(SQLModel, table=True):
    __tablename__ = "news_posts"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(sa_column=Column(Text, nullable=False))
    author: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    role_models: List["RoleModel"] = Relationship(back_populates="news_posts", link_model=NewsPostRoleModelLink)


class NewsPostCreate(SQLModel):
    title: str
    content: str
    author: Optional[str] = None
    image_url: Optional[str] = None
    role_model_ids: Optional[List[int]] = []


class NewsPostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    image_url: Optional[str] = None
    role_model_ids: Optional[List[int]] = None