# PostgreSQL database URL configuration


def run_all_initialization():
    # Create an engine to connect to the PostgreSQL database
    from alembic import command
    from alembic.config import Config

    config = Config("alembic.ini")
    command.upgrade(config, revision="head")


if __name__ == "__main__":
    run_all_initialization()
