from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_validator


# Tabela u bazi
class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    biography: Optional[str] = Field(default=None)
    field: Optional[str] = Field(default=None)
    avatar: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)