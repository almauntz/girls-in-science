from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, validator

class Registration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # GT1-30: These fields are mandatory (no Optional)
    first_name: str = Field(min_length=2)  # Name cannot be just 1 letter
    last_name: str = Field(min_length=2)
    
    # GT1-90: Email format validation
    # EmailStr automatically checks for @ and domain presence
    email: EmailStr 
    
    phone: str = Field(min_length=9)  # Basic length check for phone number
    workshop_id: int = Field(foreign_key="workshop.id")
    
    previous_experience: Optional[str] = None
    github_profile: Optional[str] = None