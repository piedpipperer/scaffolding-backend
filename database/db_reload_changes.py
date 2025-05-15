from database.connection_details import database_session
from database.models import User


def run_initialization():

    print("running initialization once tables are created:")
    # Create an engine and bind it to the database

    with database_session() as db:

        jordi = User(name="Jordi")
        helene = User(name="Helene")

        db.add(jordi)
        db.add(helene)
        # Commit the inserts
        db.commit()

    print("data inserted successfully!")


if __name__ == "__main__":
    run_initialization()
