from fastapi import HTTPException


from pydantic import BaseModel, Field
import re


class RegisterRequest(BaseModel):
    name: str
    password: str
    captcha_id: str
    captcha_answer: str
    email: str
    auth_provider: str = Field(default="local")  # "local" | "google"


def validate_user(user_info: RegisterRequest):

    # Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_info.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Password validation (example: at least 8 characters, one uppercase, one lowercase, one digit)
    if (
        len(user_info.password) < 8
        or not re.search(r"[A-Z]", user_info.password)
        or not re.search(r"[a-z]", user_info.password)
        or not re.search(r"\d", user_info.password)
    ):
        raise HTTPException(
            status_code=400,
            detail="""Password must be at least 8 characters long and contain at least one uppercase letter,
              one lowercase letter, and one digit.""",
        )
    return True
