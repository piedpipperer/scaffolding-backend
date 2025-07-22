from authlib.integrations.starlette_client import OAuth
import os

oauth = OAuth()

# Set your client IDs and secrets via environment variables
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# security = HTTPBasic()
# pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# def authenticate_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
#     # Check if username exists in the database
#     username = credentials.username
#     password = credentials.password

#     user_info = db.query(User).filter(User.name == username).one_or_none()

#     if not user_info:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Basic"},
#         )

#     # Verify password
#     if not password == user_info.password:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Basic"},
#         )

#     return username  # Return the authenticated username
