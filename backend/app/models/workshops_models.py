from datetime import datetime, timezone
from typing import Optional
import enum
from sqlmodel import SQLModel, Field


class WorkshopStatus(str, enum.Enum):
    upcoming = "upcoming"
    cancelled = "cancelled"
    completed = "completed"


class Workshop(SQLModel, table=True):
    __tablename__ = "workshops"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    location: str = Field(nullable=False)
    date: datetime = Field(nullable=False)
    capacity: int = Field(nullable=False)
    
    status: WorkshopStatus = Field(default=WorkshopStatus.upcoming)
    
    created_by_id: Optional[int] = Field(default=None, foreign_key="users.id")

    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )