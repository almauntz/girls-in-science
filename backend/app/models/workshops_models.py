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