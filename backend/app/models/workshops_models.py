from datetime import datetime, timezone
from typing import Optional
import enum
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr
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

#--elma
class Registration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    email: EmailStr 
    phone: str = Field(min_length=9)
    
    # OVDJE JE IZMJENA: 
    # 'workshops' je ime tabele kolega, a 'ID_workshop' je njihov ključ
    workshop_id: int = Field(foreign_key="workshops.ID_workshop")
    
    previous_experience: Optional[str] = None
    github_profile: Optional[str] = None

    
# L-- elma
class RegistrationCreate(SQLModel):
    first_name: str = Field(min_length=2)  # Ovdje mora biti razmak (indentacija)
    last_name: str = Field(min_length=2)
    email: EmailStr
    phone: str = Field(min_length=9)
    workshop_id: int
    previous_experience: Optional[str] = None
    github_profile: Optional[str] = None