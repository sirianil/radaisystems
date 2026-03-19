# Pydantic response schemas used by the API layer.
# from_attributes=True allows building these models directly from SQLAlchemy ORM objects.

from typing import Optional
from pydantic import BaseModel, ConfigDict

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
    latitude: Optional[float]
    longitude: Optional[float]
    schedule: Optional[str]
    days_hours: Optional[str]
    approved: Optional[str]
    expiration_date: Optional[str]

class NearestPermitResponse(PermitResponse):
    # Extends PermitResponse with a computed distance from the query point.
    distance_meters: float
