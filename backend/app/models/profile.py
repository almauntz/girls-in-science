from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.user import User

# Pivot tabela koja spaja Korisnike i Radionice (Prijave)
class WorkshopRegistration(SQLModel, table=True):
    __tablename__ = "workshop_registrations"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    workshop_id: int = Field(foreign_key="workshops.id", primary_key=True)
    registered_at: datetime = Field(default_factory=datetime.utcnow)

# Glavna tabela za Radionice
class Workshop(SQLModel, table=True):
    __tablename__ = "workshops"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    date: datetime = Field(nullable=False)
    capacity: int = Field(default=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Veza sa korisnicima preko pivot tabele
    users: List["User"] = Relationship(back_populates="workshops", link_model=WorkshopRegistration)