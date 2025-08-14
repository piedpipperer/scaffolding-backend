from uuid import uuid4
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from authentication.authentication import authenticate_user
from authentication.captcha_lib import get_captcha
from authentication.user_context import hash_password
from database.connection_details import get_db
from database.models import CaptchaEntry, User
from fastapi.responses import JSONResponse

from fastapi import HTTPException

from fastapi.responses import Response
from io import BytesIO
from pydantic import BaseModel

router = APIRouter(prefix="/user")


# this needs to be refactored, we only want to get the authenticated user info.
@router.get("/users", response_class=JSONResponse)
async def get_users(request: Request, username: str = Depends(authenticate_user), db: Session = Depends(get_db)):
    print(f"Attempting to query the database on endpoint {get_users.__name__} ...")
    users = db.query(User).all()
    print(f"Retrieved {len(users)} users.")

    users_list = [{"id_user": user.id_user, "name": user.name} for user in users]

    return users_list


@router.get("/captcha", response_class=Response)
async def get_captcha_img(db: Session = Depends(get_db)):
    captcha, captcha_image = get_captcha()

    captcha_id = uuid4()
    new_entry = CaptchaEntry(id=captcha_id, answer=captcha)
    db.add(new_entry)
    db.commit()

    img_io = BytesIO()
    captcha_image.save(img_io, format="PNG")
    img_io.seek(0)

    headers = {
        "X-Captcha-ID": str(captcha_id),
        "Access-Control-Expose-Headers": "x-captcha-id",
    }
    return Response(content=img_io.getvalue(), media_type="image/png", headers=headers)


class RegisterRequest(BaseModel):
    name: str
    password: str
    captcha_id: str
    captcha_answer: str


# if we want to implmeent in future:
# , dependencies=[Depends(RateLimiter(times=5, minutes=1))]
@router.post("/register")
async def register_user(user_info: RegisterRequest, db: Session = Depends(get_db)):

    print("received register  user", user_info)
    captcha_entry = db.query(CaptchaEntry).filter_by(id=user_info.captcha_id).first()
    if not captcha_entry or captcha_entry.answer.lower() != user_info.captcha_answer.lower():
        raise HTTPException(status_code=400, detail="Invalid or expired CAPTCHA")

    existing_user = db.query(User).filter_by(name=user_info.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or username already exists")

    hashed_pwd = hash_password(user_info.password)

    new_user = User(name=user_info.name, password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id_user}
