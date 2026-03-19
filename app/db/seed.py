# Seeds the database from the SF Mobile Food Facility Permit CSV.

import csv
import os
from sqlalchemy import insert
from app.db.session import SessionLocal
from app.models.orm import Permit

CSV_PATH = os.getenv("CSV_PATH", "raw_data/Mobile_Food_Facility_Permit_20260317.csv")

def seed(db=None):
    close_after = db is None
    if db is None:
        db = SessionLocal()
    try:
        # Skip seeding if data already exists.
        if db.query(Permit).first() is not None:
            print("Database already seeded, skipping.")
            return

        col_map = Permit.csv_column_map
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Rename CSV headers to ORM field names; drop unneeded columns; replace "" with None.
            rows = [
                {col_map[k]: (v or None) for k, v in row.items() if k in col_map}
                for row in reader
            ]

        db.execute(insert(Permit), rows)
        db.commit()
        print(f"Seeded {len(rows)} permits.")
    finally:
        if close_after:
            db.close()
