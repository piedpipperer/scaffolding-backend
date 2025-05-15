from contextlib import contextmanager
from config.conf import get_db_secret, is_running_in_lambda

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from functools import lru_cache


@lru_cache()
def get_database_url() -> str:
    # PostgreSQL database URL configuration
    if is_running_in_lambda():
        json_credents = get_db_secret()
        database_url = (
            f"postgresql://{json_credents['username']}:"
            f"{json_credents['password']}@database-1.cluster-c37doy3ngxpp."
            "eu-west-1.rds.amazonaws.com:5432/relappmidos"
        )
        # database had to be created from the query editor in aws-rds.
    else:
        database_url = "postgresql://savana:password@localhost:5432/relappmidos"

    return database_url


@contextmanager
def database_engine():
    """
    Context manager for the SQLAlchemy engine.
    Ensures the engine is properly disposed of.
    """
    engine = create_engine(get_database_url())
    try:
        yield engine
    finally:
        engine.dispose()


# Create the session factory
@contextmanager
def database_session():
    """
    Context manager for database sessions. Ensures proper cleanup of resources.
    """
    engine = create_engine(get_database_url())
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()  # Rollback transaction on error
        raise e
    finally:
        session.close()
        engine.dispose()


def get_db():
    """
    Dependency for FastAPI to provide a database session.
    """
    with database_session() as session:
        yield session
