from database.connection_details import database_session
from database.models import User


def run_initialization():

    print("running initialization once tables are created:")
    # Create an engine and bind it to the database

    with database_session() as db:

        jordi = User(name="jordi", password="1234321")  # Replace with a hashed password
        helene = User(name="helene", password="1234321")

        db.add(jordi)
        db.add(helene)
        # Commit the inserts
        db.commit()

    print("data inserted successfully!")


if __name__ == "__main__":
    run_initialization()
