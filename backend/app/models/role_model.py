from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Text
from sqlalchemy.sql import func
from app.models.news import NewsPostRoleModelLink

class RoleModel(SQLModel, table=True):
    __tablename__ = "role_models"
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    stem_field: str = Field(nullable=False)
    institution: str = Field(nullable=False)
    position: str = Field(nullable=False)
    biography: str = Field(sa_column=Column(Text, nullable=False))
    achievements: str = Field(sa_column=Column(Text, nullable=False))
    image_url: Optional[str]=Field(default=None)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    news_posts: List["NewsPost"] = Relationship(back_populates="role_models", link_model=NewsPostRoleModelLink)
    


class RoleModelCreate(SQLModel):
    first_name: str
    last_name: str
    stem_field: str
    institution: str
    position: str
    biography: str
    achievements: str
    image_url: Optional[str]=None

class RoleModelUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    stem_field: Optional[str] = None
    institution: Optional[str] = None
    position: Optional[str] = None
    biography: Optional[str] = None
    achievements: Optional[str] = None
    image_url: Optional[str]=None
