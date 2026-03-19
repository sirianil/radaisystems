# ORM model for the permits table.
# csv_column_map maps raw CSV header names to snake_case field names used in the model.

from sqlalchemy import Column, Integer, Float, String
from app.db.session import Base

class Permit(Base):
    """
    Represents the 'permits' table in the database.
    """
    __tablename__ = "permits"

    # Maps raw CSV column names to model field names
    csv_column_map = {
        "locationid": "locationid",
        "Applicant": "applicant",
        "FacilityType": "facility_type",
        "LocationDescription": "location_description",
        "Address": "address",
        "permit": "permit",
        "Status": "status",
        "FoodItems": "food_items",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Schedule": "schedule",
        "dayshours": "days_hours",
        "Approved": "approved",
        "ExpirationDate": "expiration_date",
    }

    locationid = Column(Integer, primary_key=True, index=True)
    applicant = Column(String)
    facility_type = Column(String)
    location_description = Column(String)
    address = Column(String)
    permit = Column(String)
    status = Column(String)
    food_items = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    schedule = Column(String)
    days_hours = Column(String)
    approved = Column(String)
    expiration_date = Column(String)
