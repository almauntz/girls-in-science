from sqlmodel import SQLModel, Field
from typing import Optional

# Task GT1-131: Tabela "Prijave"
class Prijava(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # GT1-96: Obavezna polja
    ime: str
    prezime: str
    email: str
    telefon: str
    radionica_id: int
    # GT1-97: Opcionalna polja
    iskustvo: Optional[str] = None
    github_nalog: Optional[str] = None