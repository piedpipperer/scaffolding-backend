from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id_user: int = Field(default=None, primary_key=True)
    name: str
    email: str  # Email field for user
    # password: str  # Hashed password field
