from contextlib import contextmanager
from config.conf import get_env_var

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from functools import lru_cache


@lru_cache()
def get_database_url() -> str:
    """
    Get the database URL from environment variables.
    Supports:
      1. Direct connection URL: DATABASE_URL or NEON_DATABASE_URL
      2. Discrete environment variables:
         DB_USER (or PG_USER), DB_PASSWORD (or PG_PWD/PG_PASSWORD),
         DB_HOST (or PG_HOST), DB_PORT (or PG_PORT), DB_NAME (or APP_NAME),
         and optional DB_SSLMODE (e.g. 'require' for Neon)
    """
    # 1. Full connection string (e.g. Neon connection string)
    db_url = get_env_var("DATABASE_URL") or get_env_var("NEON_DATABASE_URL")
    if db_url:
        return db_url

    # 2. Discrete environment variables
    user = get_env_var("DB_USER") or get_env_var("PG_USER", "postgres")
    pwd = (
        get_env_var("DB_PASSWORD")
        or get_env_var("PG_PWD")
        or get_env_var("PG_PASSWORD", "postgres")
    )
    host = get_env_var("DB_HOST") or get_env_var("PG_HOST", "localhost")
    port = get_env_var("DB_PORT") or get_env_var("PG_PORT", "5432")
    db_name = get_env_var("DB_NAME") or get_env_var("APP_NAME", "scaffolding")
    sslmode = get_env_var("DB_SSLMODE")

    base_url = f"postgresql://{user}:{pwd}@{host}:{port}/{db_name}"
    if sslmode:
        base_url = f"{base_url}?sslmode={sslmode}"
    return base_url


@contextmanager
def database_engine():
    """
    Context manager for the SQLAlchemy engine.
    Ensures the engine is properly disposed of.
    """
    engine = create_engine(get_database_url(), connect_args={"connect_timeout": 2}, echo=True)
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
