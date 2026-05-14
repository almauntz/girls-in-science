from datetime import datetime
from enum import Enum
from typing import Optional
from dns import enum
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, Enum as SAEnum, func


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
    status: WorkshopStatus = Field(
        default=WorkshopStatus.upcoming,
        sa_column=Column(SAEnum(WorkshopStatus), default=WorkshopStatus.upcoming)
    )
    created_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )