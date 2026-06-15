import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Integer, Enum as SAEnum, DateTime
from sqlalchemy.sql import func
from app.database import Base


class UserRole(str, enum.Enum):
    member = "member"
    mentor = "mentor"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.member, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
