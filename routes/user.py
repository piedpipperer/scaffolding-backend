from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from authentication.authentication import authenticate_user
from database.connection_details import get_db
from database.models import User

router = APIRouter(prefix="/user")


@router.get("/users", response_class=HTMLResponse)
async def get_users(request: Request, username: str = Depends(authenticate_user), db: Session = Depends(get_db)):
    print(f"Attempting to query the database on endpoint {get_users.__name__} ...")
    users = db.query(User).all()
    print(f"Retrieved {len(users)} users.")

    html_response = "".join(f'<option value="{user.id_user}">{user.name}</option>' for user in users)

    return html_response
