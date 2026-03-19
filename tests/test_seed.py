# Tests for the database seed function.
# Uses a temporary CSV file and an in-memory SQLite database to avoid touching the real data.

import pytest
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from app.db.session import Base
from app.models.orm import Permit
from app.db.seed import seed


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


SAMPLE_CSV = """locationid,Applicant,FacilityType,LocationDescription,Address,permit,Status,FoodItems,Latitude,Longitude,Schedule,dayshours,Approved,ExpirationDate
1001,Taco Truck,Truck,Near Park,123 Main St,24MFF-00001,APPROVED,Tacos,37.77,-122.41,http://schedule.url,Mo-Fr:8AM-5PM,20240101,2025 Jan 15 12:00:00 AM
1002,Snack Cart,Push Cart,,456 Oak Ave,24MFF-00002,REQUESTED,Chips,37.78,-122.42,http://schedule.url,,20240201,
"""

@pytest.fixture
def csv_path(tmp_path):
    path = tmp_path / "test_permits.csv"
    path.write_text(SAMPLE_CSV)
    return str(path)

# Unit test for correct number of rows
def test_seed_inserts_rows(db, csv_path):
    with patch("app.db.seed.CSV_PATH", csv_path):
        seed(db)
    assert db.query(Permit).count() == 2

# Unit test for mapping db table column names to csv columns
def test_seed_maps_columns_correctly(db, csv_path):
    with patch("app.db.seed.CSV_PATH", csv_path):
        seed(db)
    permit = db.query(Permit).filter_by(locationid=1001).first()
    assert permit.applicant == "Taco Truck"
    assert permit.facility_type == "Truck"
    assert permit.status == "APPROVED"
    assert permit.latitude == 37.77

# Unit test for empty csv values
def test_seed_stores_null_for_missing_values(db, csv_path):
    with patch("app.db.seed.CSV_PATH", csv_path):
        seed(db)
    permit = db.query(Permit).filter_by(locationid=1002).first()
    assert permit.location_description is None
    assert permit.approved is not None

# Unit test to ensure seeding only once
def test_seed_skips_if_already_seeded(db, csv_path):
    with patch("app.db.seed.CSV_PATH", csv_path):
        seed(db)
        seed(db)
    assert db.query(Permit).count() == 2
