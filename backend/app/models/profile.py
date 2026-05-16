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

# Shema za ažuriranje profila
class ProfileUpdate(SQLModel):
    full_name: Optional[str] = None
    biography: Optional[str] = None
    field: Optional[str] = None

    # Provjerava da li je uneseno ime validno (ne smije biti prazan string)
    @field_validator('full_name')
    @classmethod
    def name_not_empty(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError('Ime ne smije biti prazno')
        return v

    # Ograničava biografiju na 500 karaktera
    @field_validator('biography')
    @classmethod
    def biography_max_length(cls, v):
        if v is not None and len(v) > 500:
            raise ValueError('Biografija ne smije biti duža od 500 karaktera')
        return v
    
# Shema za prikaz profila
class ProfileResponse(SQLModel):
    id: int
    user_id: int
    full_name: str
    email: str
    biography: Optional[str] = None
    field: Optional[str] = None
    avatar: Optional[str] = None
    role: str

    class Config:
        from_attributes = True
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
