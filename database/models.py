from datetime import datetime

from typing import Optional
import uuid
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "user"
    id_user: int = Field(default=None, primary_key=True)
    name: Optional[str] = None
    email: str = Field(unique=True)
    password: Optional[str] = None  # empty means OAuth user
    provider: Optional[str] = "local"  # "google" or "local"


class CaptchaEntry(SQLModel, table=True):
    __tablename__ = "captcha_entry"
    id: uuid.UUID = Field(default=None, primary_key=True)
    answer: str
    year: int = Field(default_factory=lambda: datetime.utcnow().year)
    month: int = Field(default_factory=lambda: datetime.utcnow().month)
