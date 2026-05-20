import enum
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy import DateTime
class UserRole(str, enum.Enum):
    member = "member"
    mentor = "mentor"
    admin = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    full_name: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)
    role: UserRole = Field(
        default=UserRole.member,
        sa_column=Column(SAEnum(UserRole), default=UserRole.member)
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
