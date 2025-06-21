from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from authentication.authentication import authenticate_user
from database.connection_details import get_db
from database.models import User
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/user")


@router.get("/users", response_class=JSONResponse)
async def get_users(request: Request, username: str = Depends(authenticate_user), db: Session = Depends(get_db)):
    print(f"Attempting to query the database on endpoint {get_users.__name__} ...")
    users = db.query(User).all()
    print(f"Retrieved {len(users)} users.")

    users_list = [{"id_user": user.id_user, "name": user.name} for user in users]

    return users_list
