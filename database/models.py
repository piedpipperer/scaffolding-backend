from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id_user: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str  # Hashed password field
