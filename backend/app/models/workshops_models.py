from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import validator, EmailStr # EmailStr je najbolji za GT1-90

# Task GT1-131: Tabela "Prijave"
class Prijava(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # GT1-96 & GT1-30: Validacija obaveznih polja (min_length sprečava prazne stringove)
    ime: str = Field(min_length=2, index=True)
    prezime: str = Field(min_length=2)
    
    # GT1-90: Validacija email formata
    # Koristimo EmailStr koji automatski provjerava format (npr. mora imati @ i domenu)
    email: EmailStr 
    
    # GT1-30: Telefon je obavezan, dodajemo provjeru minimalne dužine
    telefon: str = Field(min_length=9)
    
    radionica_id: int = Field(foreign_key="workshop.id")
    
    # GT1-97: Opcionalna polja ostaju ista
    iskustvo: Optional[str] = None
    github_nalog: Optional[str] = None

    # GT1-90: Ako profesorica insistira na ručnoj funkciji za validaciju emaila:
    @validator("email")
    def email_must_contain_at(cls, v):
        if "@" not in v:
            raise ValueError("Email mora sadržavati @ simbol")
        return v