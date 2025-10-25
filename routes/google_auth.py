from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from authentication.jwt import create_app_jwt
from config.conf import get_env_var
from database.models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from database.connection_details import get_db


GOOGLE_CLIENT_ID = get_env_var("GOOGLE_CLIENT_ID")
router = APIRouter(prefix="/google")


@router.post("/auth")
async def auth_google(credential: str, db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(credential, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    email = idinfo.get("email")
    name = idinfo.get("name")
    sub = idinfo.get("sub")  # Google's user unique ID

    user = db.query(User).filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, password=None, provider="google")
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # ✅ Existing user found, gonna override its config:
        if user.provider == "google":
            # Upgrade to Google-based login
            user.provider = "google"
            db.commit()
            db.refresh(user)
        elif user.provider == "local":
            # Just ensure provider_id is up to date (defensive)
            if not user.provider_id:
                user.provider_id = sub
                db.commit()

    # Create your app’s session or JWT for this user
    return {"access_token": create_app_jwt(user), "user": {"id": user.id_user, "name": user.name, "email": user.email}}