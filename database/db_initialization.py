from database.connection_details import database_engine
from database.db_reload_changes import run_initialization
from database.models import (
    Base,
)

# PostgreSQL database URL configuration


def run_all_initialization():
    # Create an engine to connect to the PostgreSQL database

    with database_engine() as engine:
        print("about to drop and create tables:")
        # Drop all tables from your models if they exist
        Base.metadata.drop_all(bind=engine)
        # Create all tables from your models
        Base.metadata.create_all(bind=engine)

    print("Tables have been created successfully!")

    run_initialization()


if __name__ == "__main__":
    run_all_initialization()
