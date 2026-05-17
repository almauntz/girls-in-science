from datetime import datetime, timezone
from typing import Optional
import enum
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from datetime import datetime
class WorkshopStatus(str, enum.Enum):
    upcoming = "upcoming"
    cancelled = "cancelled"
    completed = "completed"

class WorkshopBase(SQLModel):
    title: str
    description: str
    location: str
    date: datetime
    end_time: datetime
    capacity: int

class Workshop(WorkshopBase, table=True):
    __tablename__ = "workshops"

    ID_workshop: Optional[int] = Field(default=None, primary_key=True)
    status: WorkshopStatus = Field(default=WorkshopStatus.upcoming)
    created_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


### Schemas -------------------------------------------------------------------
class WorkshopCreate(BaseModel):
    title: str
    description: str
    location: str
    date: datetime
    end_time: datetime
    capacity: int

class WorkshopUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = None

class WorkshopRead(BaseModel):
    ID_workshop: int
    title: str
    description: str
    location: str
    date: datetime
    end_time: datetime
    capacity: int
    status: WorkshopStatus
    created_by_id: Optional[int]
    created_at: Optional[datetime]
    class Config:
        from_attributes = True

class WorkshopList(BaseModel):
    title: str
    date: datetime
    location: str
    class Config:
        from_attributes = True

class WorkshopDetailRead(BaseModel):
    ID_workshop: int
    title: str
    description: str
    date: datetime
    end_time: datetime
    capacity: int
    status: WorkshopStatus
    organizer_name:str
    organizer_email:str
    class Config:
        from_attributes = True

class Registration(SQLModel, table=True):
    __tablename__ = "registrations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # GT1-30: These fields are mandatory (no Optional)
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    
    # GT1-90: Email format validation
    email: EmailStr 
    
    phone: str = Field(min_length=9, max_length=20)
    user_id: int = Field(foreign_key="users.id")
    workshop_id: int = Field(foreign_key="workshops.ID_workshop")
    
    # OPCIONALNA POLJA
    previous_experience: Optional[str] = Field(default=None, max_length=1000)
    github_profile: Optional[str] = Field(default=None, max_length=255)
    
    # META POLJA
    status: ApplicationStatus = Field(default=ApplicationStatus.pending)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    confirmed_at: Optional[datetime] = Field(default=None)


### Registration Schemas -------------------------------------------------------------------

class RegistrationCreate(BaseModel):
    """Schema za slanje registracije"""
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=9, max_length=20)
    previous_experience: Optional[str] = Field(default=None, max_length=1000)
    github_profile: Optional[str] = Field(default=None, max_length=255)
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Marija",
                "last_name": "Horvat",
                "email": "marija@example.com",
                "phone": "+385981234567",
                "previous_experience": "Znam osnove Python-a",
                "github_profile": "https://github.com/marija-horvat"
            }
        }

class RegistrationRead(BaseModel):
    """Schema za čitanje registracije"""
    id: int
    user_id: int
    workshop_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    previous_experience: Optional[str]
    github_profile: Optional[str]
    status: str
    registered_at: datetime
    confirmed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class RegistrationList(BaseModel):
    """Schema za prikaz liste registracija"""
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: str
    registered_at: datetime
    previous_experience: Optional[str]
    
    class Config:
        from_attributes = True
