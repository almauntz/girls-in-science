from datetime import datetime, timezone
from typing import Optional
import enum
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
  
class WorkshopStatus(str, enum.Enum):
    upcoming = "upcoming"
    cancelled = "cancelled"
    completed = "completed"

class ProposalStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

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
    #created_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    created_by_id: Optional[int] = Field(default=None)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# Klasa za prijedlog radionice od strane korisnice
class WorkshopProposal(SQLModel, table=True):
    __tablename__ = "workshop_proposals"
 
    id: Optional[int] = Field(default=None, primary_key=True)
 
    title: str
    description: str
 
    proposed_by_id: int = Field()
    proposed_by_email: str
 
    status: ProposalStatus = Field(default=ProposalStatus.pending)
 
    admin_note: Optional[str] = None
 
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

### Schemas za Workshop proposal -----------------------------------------------

class ProposalCreate(BaseModel):
    title: str
    description: str

class ProposalRead(BaseModel):
    id: int
    title: str
    description: str
    proposed_by_id: int
    proposed_by_email: str
    status: ProposalStatus
    admin_note: Optional[str]
    created_at: Optional[datetime]
 
    class Config:
        from_attributes = True

class ProposalUserRead(BaseModel):
    id: int
    title: str
    description: str
    status: ProposalStatus
    admin_note: Optional[str]
    created_at: Optional[datetime]
    class Config:
        from_attributes = True

class ProposalReject(BaseModel):
    admin_note: Optional[str] = None

class ProposalApprove(BaseModel):
    admin_note: Optional[str] = None
    create_workshop: bool = False
    location: Optional[str] = None
    date: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = None 

### ---------------------------------------------------------------------------

class WorkshopList(BaseModel):
    ID_workshop: int
    title: str
    date: datetime
    location: str
    free_spots: int
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
    free_spots:int
    class Config:
        from_attributes = True

class Registration(Base):
    __tablename__ = "registration"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    workshop_id = Column(Integer, nullable=False)

    previous_experience = Column(String, nullable=True)
    github_profile = Column(String, nullable=True)
    
class RegistrationCreate(SQLModel):
    first_name: str = Field(min_length=2) 
    last_name: str = Field(min_length=2)
    email: EmailStr
    phone: str = Field(min_length=9)
    workshop_id: int
    previous_experience: Optional[str] = None
    github_profile: Optional[str] = None
