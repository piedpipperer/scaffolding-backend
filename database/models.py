from datetime import datetime

from typing import Optional
import uuid
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "user"
    id_user: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str  # Hashed password field


class CaptchaEntry(SQLModel, table=True):
    __tablename__ = "captcha_entry"
    id: uuid.UUID = Field(default=None, primary_key=True)
    answer: str
    year: int = Field(default_factory=lambda: datetime.utcnow().year)
    month: int = Field(default_factory=lambda: datetime.utcnow().month)
