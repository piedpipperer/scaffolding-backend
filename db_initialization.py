from database.db_initialization import run_all_initialization

if __name__ == "__main__":
    print("Running database initialization (Alembic migrations)...")
    run_all_initialization()
    print("Database initialization complete.")

