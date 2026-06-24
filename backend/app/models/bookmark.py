from typing import Optional
from sqlmodel import SQLModel, Field

class Bookmark(SQLModel, table=True):
    __tablename__ = "bookmarks"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    role_model_id: int = Field(foreign_key="role_models.id", nullable=False)