from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from authentication.authentication import get_current_user
from authentication.jwt import create_app_jwt
from config.conf import get_env_var
from config.connectivity import test_connectivity
from database.models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from database.connection_details import get_db
from authentication.authentication import get_current_user


GOOGLE_CLIENT_ID = get_env_var("GOOGLE_CLIENT_ID")
router = APIRouter(prefix="/google")


class GoogleAuthRequest(BaseModel):
    credential: str


@router.post("/auth")
async def auth_google(payload: GoogleAuthRequest, db: Session = Depends(get_db)):

    print("request received:", payload)
    try:
        test_connectivity()
        print("about to try call of google authorization", payload.credential, requests.Request(), GOOGLE_CLIENT_ID)
        idinfo = id_token.verify_oauth2_token(payload.credential, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    print("got idinfo", idinfo)

    email = idinfo.get("email")
    name = idinfo.get("name")
    # sub = idinfo.get("sub")  # Google's user unique ID

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
            db.commit()

    # Create your app’s session or JWT for this user

    google_auth_return = {
        "access_token": create_app_jwt(user),
        "user": {"id": user.id_user, "name": user.name, "email": user.email},
    }
    print("returning:", google_auth_return)
    return google_auth_return


@router.post("/link/google")
async def link_google(
    payload: GoogleAuthRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):

    idinfo = id_token.verify_oauth2_token(payload.credential, requests.Request(), GOOGLE_CLIENT_ID)
    email = idinfo.get("email")

    # sanity check: emails must match
    if email != current_user.email:
        raise HTTPException(status_code=400, detail="Google email does not match account email")

    current_user.provider = "google"
    db.commit()

    return {"message": "Google account linked successfully"}


@router.post("/unlink/google")
async def unlink_google(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.provider != "google":
        raise HTTPException(status_code=400, detail="No Google link found")

    current_user.provider = "local"
    current_user.provider_id = None
    db.commit()

    return {"message": "Google account unlinked"}
