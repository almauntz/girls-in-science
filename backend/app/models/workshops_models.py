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
    capacity: int

class Workshop(WorkshopBase, table=True):
    __tablename__ = "workshops"

    ID_workshop: Optional[int] = Field(default=None, primary_key=True)
    status: WorkshopStatus = Field(default=WorkshopStatus.upcoming)
    created_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


### Schemas ---------------------------------------------------------------------
class WorkshopCreate(BaseModel):
    title: str
    description: str
    location: str
    date: datetime
    capacity: int

class WorkshopUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date: Optional[datetime] = None
    capacity: Optional[int] = None

class WorkshopRead(BaseModel):
    ID_workshop: int
    title: str
    description: str
    location: str
    date: datetime
    capacity: int
    status: WorkshopStatus
    created_by_id: Optional[int]
    created_at: Optional[datetime]
    class Config:
        from_attributes = True
