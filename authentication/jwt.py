# auth_utils.py
from config.conf import get_env_var
from database.models import User
import jwt
from datetime import datetime, timedelta


JWT_SECRET_KEY = get_env_var("JWT_SECRET_KEY") 
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24  # 1 day


def create_app_jwt(user: User) -> str:
    payload = {
        "sub": str(user.id_user),
        "email": user.email,
        "name": user.name,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verify_app_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None