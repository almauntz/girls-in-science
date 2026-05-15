from sqlmodel import SQLModel, Field
from typing import Optional

class RoleModel(SQLModel, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    stem_field: str
    institution: str
    biography: Optional[str]=None
    achievements: Optional[str]=None