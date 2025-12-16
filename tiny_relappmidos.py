from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from config.conf import HEADERS, is_running_in_lambda
from database.connection_details import get_database_url
from routes import google_auth, user
from mangum import Mangum
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


def tell_me_handler(app: FastAPI):
    if not is_running_in_lambda():
        return None
    return Mangum(app)


# Global variables for the database engine and session factory
engine = None
SessionLocal = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Define the lifespan context manager for FastAPI.
    Initialize and dispose of resources during app lifecycle.
    """
    global engine, SessionLocal
    # Initialize the database engine and session factory during app startup
    engine = create_engine(get_database_url(), pool_size=10, max_overflow=5, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("Database engine and session factory initialized.")

    # Yield control to the application
    yield

    # Dispose of the engine during app shutdown
    if engine:
        engine.dispose()
        print("Database engine disposed.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.options("/{path:path}")
async def handle_options(request: Request):
    headers = HEADERS
    headers["Access-Control-Allow-Origin"] = request.headers.get("origin", "*")
    headers["Content-Type"] = "application/json"
    print("OPTIONS Response Headers:", headers)
    return JSONResponse(content={"message": "CORS preflight response"}, status_code=200, headers=headers)


handler = tell_me_handler(app)

app.include_router(user.router)
app.include_router(google_auth.router)
# app.include_router(count_relappmidos.router)


def lambda_handler(event, context):
    # Extract the path from the event object for logging
    # The structure of the event object can vary depending on the Lambda trigger.
    # For API Gateway proxy integration, the path is usually in event['path'] or event['requestContext']['path']
    path = event.get("path", "N/A")
    http_method = event.get("httpMethod", "N/A")
    print(f"Calling endpoint: {http_method} {path}")
    return handler(event, context)  # type: ignore
