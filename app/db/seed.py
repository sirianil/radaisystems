# Seeds the database from the SF Mobile Food Facility Permit CSV.
# Only runs if the permits table is empty, so it is safe to call on every startup.

import pandas as pd
from app.db.session import SessionLocal
from app.models.orm import Permit

CSV_PATH = "/code/raw_data/Mobile_Food_Facility_Permit_20260317.csv"

def seed(db=None):
    """Load permit records from CSV into the database.

    Accepts an optional db session so tests can pass their own session.
    If none is provided, opens and closes one internally.
    """
    close_after = db is None
    if db is None:
        db = SessionLocal()
    try:
        # Skip seeding if data already exists.
        if db.query(Permit).first() is not None:
            print("Database already seeded, skipping.")
            return

        # Read only the columns we care about, then rename to match ORM field names.
        df = pd.read_csv(CSV_PATH, usecols=Permit.csv_column_map.keys())
        df = df.rename(columns=Permit.csv_column_map)
        # Replace NaN with None so SQLAlchemy stores NULL instead of the string "nan".
        df = df.where(pd.notna(df), None)

        db.bulk_insert_mappings(Permit, df.to_dict(orient="records"))
        db.commit()
        print(f"Seeded {len(df)} permits.")
    finally:
        if close_after:
            db.close()
