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

    @field_validator('full_name')
    @classmethod
    def name_not_empty(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError('Ime ne smije biti prazno')
        return v

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