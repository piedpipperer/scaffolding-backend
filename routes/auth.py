from fastapi import APIRouter, Depends, Request
from auth import oauth
from database.connection_details import get_db
from sqlalchemy.orm import Session
from database.models import User

router = APIRouter(prefix="/login")


@router.get("/{provider}")
async def login(request: Request, provider: str):
    redirect_uri = request.url_for("auth_callback", provider=provider)
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)


@router.get("/callback/{provider}")
async def auth_callback(request: Request, provider: str, db: Session = Depends(get_db)):
    token = await oauth.create_client(provider).authorize_access_token(request)

    if provider == "google":
        user_info = await oauth.google.parse_id_token(request, token)
    # elif provider == "facebook":
    #     resp = await oauth.facebook.get("me?fields=id,name,email", token=token)
    #     user_info = resp.json()
    else:
        return {"error": "Unsupported provider"}

    email = user_info.get("email")
    name = user_info.get("name")

    # Upsert user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=name)
        db.add(user)
        db.commit()

    # You can issue a session token or JWT here
    return {"email": email, "name": name}
