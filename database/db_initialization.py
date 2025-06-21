from database.connection_details import database_engine
from database.db_reload_changes import run_initialization
from database.models import (
    Base,
)

# PostgreSQL database URL configuration


def run_all_initialization():
    # Create an engine to connect to the PostgreSQL database

    # import socket
    # import logging

    # # Enable debug logs for socket operations
    # def enable_socket_debugging():
    #     try:
    #         import sys
    #         import http.client as http_client
    #     except ImportError:
    #         import http.client as http_client  # Python 3 only

    #     http_client.HTTPConnection.debuglevel = 1

    #     logging.basicConfig()
    #     logging.getLogger().setLevel(logging.DEBUG)
    #     requests_log = logging.getLogger("requests.packages.urllib3")
    #     requests_log.setLevel(logging.DEBUG)
    #     requests_log.propagate = True

    #     socket.setdefaulttimeout(5)  # Optional: Set a socket timeout globally

    # enable_socket_debugging()

    print("about to create engine")
    with database_engine() as engine:
        print("engine created")

        with engine.connect():

            print("about to drop and create tables:")
            # Drop all tables from your models if they exist
            try:
                Base.metadata.drop_all(bind=engine)
            except Exception as e:
                print("Drop failed:", e)

            # Create all tables from your models
            Base.metadata.create_all(bind=engine)

    print("Tables have been created successfully!")

    run_initialization()


if __name__ == "__main__":
    run_all_initialization()
