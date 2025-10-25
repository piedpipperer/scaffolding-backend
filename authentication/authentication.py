from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from passlib.context import CryptContext

from authentication.jwt import decode_jwt_token
from authentication.user_context import verify_password
from database.models import User
from database.connection_details import get_db  # Assuming you have a database session dependency

security = HTTPBearer()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    email = credentials.username
    password = credentials.password

    user_info = db.query(User).filter(User.email == email).one_or_none()

    if not user_info or not verify_password(password, user_info.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return email  # Return the authenticated username


def get_current_user(credentials=Depends(security), db: Session = Depends(get_db)):

    token = credentials.credentials  # from "Authorization: Bearer <token>"
    print(f"🔍 Incoming token: {token[:30]}...")
    payload = decode_jwt_token(token)

    user_email = payload.get("email")
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
