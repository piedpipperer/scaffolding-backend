from uuid import uuid4
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import base64

from authentication.authentication import get_current_user
from authentication.captcha_lib import get_captcha
from authentication.jwt import create_app_jwt
from authentication.user_context import hash_password, verify_password
from database.connection_details import get_db
from database.models import CaptchaEntry, User
from fastapi.responses import JSONResponse

from fastapi import HTTPException

from io import BytesIO
from pydantic import BaseModel

from use_cases.create_user import RegisterRequest, validate_user

router = APIRouter(prefix="/user")

# with basic authentication.
# # this needs to be refactored, we only want to get the authenticated user info.
# @router.get("/former_users", response_class=JSONResponse)
# async def former_get_users(request: Request, email: str = Depends(authenticate_user), db: Session = Depends(get_db)):
#     print(f"Attempting to query the database on endpoint {get_users.__name__} ...")
#     users = db.query(User).all()
#     print(f"Retrieved {len(users)} users.")

#     users_list = [{"id_user": user.id_user, "name": user.name} for user in users]

#     return users_list


# this needs to be refactored, we only want to get the authenticated user info.
@router.get("/users", response_class=JSONResponse)
async def get_users(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    print(f"Authenticated user: {current_user.email}")
    users = db.query(User).all()
    print(f"Retrieved {len(users)} users.")

    users_list = [{"id_user": user.id_user, "name": user.name, "user_type": user.user_type} for user in users]

    return users_list


@router.get("/captcha")
async def get_captcha_img(db: Session = Depends(get_db)):
    captcha, captcha_image = get_captcha()

    captcha_id = uuid4()
    new_entry = CaptchaEntry(id=captcha_id, answer=captcha)
    db.add(new_entry)
    db.commit()

    img_io = BytesIO()
    captcha_image.save(img_io, format="PNG")
    img_io.seek(0)

    content = img_io.getvalue()

    return {
        "captcha_id": str(captcha_id),
        "image_base64": base64.b64encode(content).decode("utf-8"),
    }


# if we want to implmeent in future:
# , dependencies=[Depends(RateLimiter(times=5, minutes=1))]
@router.post("/register")
async def register_user(user_info: RegisterRequest, db: Session = Depends(get_db)):

    print("received register  user", user_info)
    captcha_entry = db.query(CaptchaEntry).filter_by(id=user_info.captcha_id).first()
    if not captcha_entry or captcha_entry.answer.lower() != user_info.captcha_answer.lower():
        raise HTTPException(status_code=400, detail="Invalid or expired CAPTCHA")

    if not validate_user(user_info):
        raise HTTPException(status_code=400, detail="Invalid user data")
    existing_user = db.query(User).filter_by(email=user_info.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or username already exists")

    hashed_pwd = hash_password(user_info.password)

    new_user = User(name=user_info.name, email=user_info.email, password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # pending the autologin: (jwt...)

    return {
        "access_token": create_app_jwt(new_user),
        "message": "User created successfully",
        "user_id": new_user.id_user,
    }


@router.get("/token/verify")
async def verify_token(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id_user, "email": current_user.email, "provider": current_user.provider}


@router.delete("/delete_user")
async def delete_user(user_id: int = None, db: Session = Depends(get_db), username: User = Depends(get_current_user)):
    if not user_id:
        raise HTTPException(status_code=400, detail="Provide either user_id or name to delete a user")

    # Delete FacePartLick entries for this user
    db.query(FacePartLick).filter(FacePartLick.user_id == user_id).delete()
    # Delete the user
    user_deleted = db.query(User).filter(User.id_user == user_id).delete()
    db.commit()

    if user_deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=req.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.password:
        raise HTTPException(status_code=403, detail="Password login disabled for Google users")

    if not verify_password(req.password, user.password):

        if user.provider == "google":
            raise HTTPException(
                status_code=403, detail="This account uses Google Sign-In. Please log in with Google instead."
            )
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_app_jwt(user)
    return {"access_token": token}
