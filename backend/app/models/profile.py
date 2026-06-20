from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, field_validator
from app.models.user import User, UserRole


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str

class LanguageEntry(BaseModel):
    name: str
    level: Optional[str] = ""  

class ExperienceEntry(BaseModel):
    title: str
    organization: Optional[str] = ""
    location: Optional[str] = None
    start_date: Optional[str] = ""
    end_date: Optional[str] = None
    description: Optional[str] = None

class EducationEntry(BaseModel):
    degree: str
    institution: Optional[str] = ""
    start_date: Optional[str] = ""
    end_date: Optional[str] = None
    description: Optional[str] = None


# Tabela u bazi
class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    biography: Optional[str] = Field(default=None)
    field: Optional[str] = Field(default=None)
    avatar: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    location: Optional[str] = Field(default=None, nullable=True)
    deactivated_by: Optional[str] = Field(default=None)

    # Privacy polja
    show_biography: bool = Field(default=True)
    show_field: bool = Field(default=True)
    show_location: bool = Field(default=True)

    languages: Optional[str] = Field(default=None)    
    experience: Optional[str] = Field(default=None)   
    education: Optional[str] = Field(default=None)    
    skills: Optional[str] = Field(default=None)      
    linkedin_url: Optional[str] = Field(default=None)
    github_url: Optional[str] = Field(default=None)
    twitter_url: Optional[str] = Field(default=None)

# Shema za ažuriranje profila
class ProfileUpdate(SQLModel):
    full_name: Optional[str] = None
    biography: Optional[str] = None
    field: Optional[str] = None
    location: Optional[str] = Field(default=None, nullable=True)
    email: Optional[str] = None

    # Privacy polja
    show_biography: Optional[bool] = None
    show_field: Optional[bool] = None
    show_location: Optional[bool] = None

    languages: Optional[List[LanguageEntry]] = None
    experience: Optional[List[ExperienceEntry]] = None
    education: Optional[List[EducationEntry]] = None 
    skills: Optional[List[str]] = None    
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    twitter_url: Optional[str] = None

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
    location: Optional[str] = Field(default=None, nullable=True)
    biography: Optional[str] = None
    field: Optional[str] = None
    avatar: Optional[str] = None
    role: str

    # Privacy polja
    show_biography: bool = True
    show_field: bool = True
    show_location: bool = True

    languages: Optional[List[LanguageEntry]] = None
    experience: Optional[List[ExperienceEntry]] = None
    education: Optional[List[EducationEntry]] = None  
    skills: Optional[List[str]] = None    
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    twitter_url: Optional[str] = None

    class Config:
        from_attributes = True

# Pivot tabela - kept in workshops_models.py; removed from here to avoid duplicate table definition


class UpdateRoleRequest(BaseModel):
    role: UserRole

# Shema za javni prikaz profila
class PublicProfileResponse(SQLModel):
    full_name: str
    field: Optional[str] = None
    biography: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = Field(default=None, nullable=True)
    languages: Optional[List[LanguageEntry]] = None
    experience: Optional[List[ExperienceEntry]] = None
    education: Optional[List[EducationEntry]] = None    
    skills: Optional[List[str]] = None    
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    twitter_url: Optional[str] = None

    class Config:
        from_attributes = True