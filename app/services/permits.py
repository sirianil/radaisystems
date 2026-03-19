from math import radians, sin, cos, sqrt, atan2
from typing import Optional
from sqlalchemy.orm import Session
from app.models.orm import Permit
from app.models.schemas import NearestPermitResponse

EARTH_RADIUS_METERS = 6_371_000
BOUNDING_BOX_DEGREES = 0.1  # ~11km

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_METERS * atan2(sqrt(a), sqrt(1 - a))

def search_by_applicant(
    db: Session,
    applicant: str,
    status: Optional[str] = None,
) -> list[Permit]:
    query = db.query(Permit).filter(Permit.applicant == applicant)
    if status:
        query = query.filter(Permit.status.ilike(status))
    return query.all()

def search_by_address(db: Session, address: str) -> list[Permit]:
    return db.query(Permit).filter(Permit.address.ilike(f"%{address}%")).all()

def nearest_permits(
    db: Session,
    lat: float,
    lon: float,
    status: Optional[str] = "APPROVED",
) -> list[NearestPermitResponse]:
    query = db.query(Permit).filter(
        Permit.latitude.isnot(None),
        Permit.longitude.isnot(None),
        Permit.latitude.between(lat - BOUNDING_BOX_DEGREES, lat + BOUNDING_BOX_DEGREES),
        Permit.longitude.between(lon - BOUNDING_BOX_DEGREES, lon + BOUNDING_BOX_DEGREES),
    )
    if status:
        query = query.filter(Permit.status.ilike(status))

    candidates = query.all()
    ranked = sorted(candidates, key=lambda p: haversine(lat, lon, p.latitude, p.longitude))

    results = []
    for permit in ranked[:5]:
        data = permit.__dict__.copy()
        data["distance_meters"] = haversine(lat, lon, permit.latitude, permit.longitude)
        results.append(NearestPermitResponse(**data))

    return results
