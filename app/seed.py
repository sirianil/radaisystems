import pandas as pd
from app.database import SessionLocal
from app.models import Permit

CSV_PATH = "/code/raw_data/Mobile_Food_Facility_Permit_20260317.csv"

def seed(db=None):
    close_after = db is None
    if db is None:
        db = SessionLocal()
    try:
        if db.query(Permit).first() is not None:
            print("Database already seeded, skipping.")
            return

        df = pd.read_csv(CSV_PATH, usecols=Permit.csv_column_map.keys())
        df = df.rename(columns=Permit.csv_column_map)
        df = df.where(pd.notna(df), None)

        db.bulk_insert_mappings(Permit, df.to_dict(orient="records"))
        db.commit()
        print(f"Seeded {len(df)} permits.")
    finally:
        if close_after:
            db.close()
