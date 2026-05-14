from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.workshops_models import WorkshopStatus

router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.get("/")
def workshops_placeholder():
    return {"message": "Workshops router is working — Team 1 builds here"}


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
    id: int
    title: str
    description: str
    location: str
    date: datetime
    capacity: int
    status: WorkshopStatus
    created_by_id: Optional[int]
    created_at: Optional[datetime]