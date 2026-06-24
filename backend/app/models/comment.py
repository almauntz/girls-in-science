from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    news_post_id: int = Field(foreign_key="news_posts.id", nullable=False)
    user_full_name: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

class CommentCreate(SQLModel):
    content: str

class CommentRead(SQLModel):
    id: int
    content: str
    user_id: int
    user_full_name: str
    created_at: Optional[datetime] = None