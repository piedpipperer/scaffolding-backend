# PostgreSQL database URL configuration


def run_all_initialization():
    # Create an engine to connect to the PostgreSQL database
    from database.connection_details import get_database_url
    from alembic import command
    from alembic.config import Config

    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", str(get_database_url()))
    command.upgrade(config, revision="head")


if __name__ == "__main__":
    run_all_initialization()
