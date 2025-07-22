from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from authentication.authentication import authenticate_user
from authentication.user_context import hash_password
from database.connection_details import get_db
from database.models import User
from fastapi.responses import JSONResponse

from fastapi import HTTPException
from fastapi_limiter.depends import RateLimiter


router = APIRouter(prefix="/user")


# this needs to be refactored, we only want to get the authenticated user info.
@router.get("/users", response_class=JSONResponse)
async def get_users(request: Request, username: str = Depends(authenticate_user), db: Session = Depends(get_db)):
    print(f"Attempting to query the database on endpoint {get_users.__name__} ...")
    users = db.query(User).all()
    print(f"Retrieved {len(users)} users.")

    users_list = [{"id_user": user.id_user, "name": user.name} for user in users]

    return users_list


@router.post("/register", dependencies=[Depends(RateLimiter(times=5, minutes=1))])
async def register_user(request: Request, user: User, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(name=user.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or username already exists")

    hashed_pwd = hash_password(user.password)

    new_user = User(name=user.name, password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id_user}
