from typing import Optional
from sqlalchemy import Column, Integer, Float, String
from pydantic import BaseModel, ConfigDict
from app.database import Base


class Permit(Base):
    __tablename__ = "permits"

    # Maps CSV column names to model field names
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

class PermitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    locationid: int
    applicant: Optional[str]
    facility_type: Optional[str]
    location_description: Optional[str]
    address: Optional[str]
    permit: Optional[str]
    status: Optional[str]
    food_items: Optional[str]
    schedule: Optional[str]
    days_hours: Optional[str]
    approved: Optional[str]
    expiration_date: Optional[str]
