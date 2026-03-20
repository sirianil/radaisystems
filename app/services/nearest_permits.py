from math import radians, sin, cos, sqrt, atan2
from typing import Optional
from sqlalchemy.orm import Session
from app.models.orm import Permit
from app.models.schemas import NearestPermitResponse

EARTH_RADIUS_METERS = 6_371_000
BOUNDING_BOX_DEGREES = 0.1       # Initial bounding box (~11km), covers most of SF.
MAX_BOUNDING_BOX_DEGREES = 0.5   # Cap at ~55km (approximately greater SF Bay Area).


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return the great-circle distance in meters between two lat/lon points."""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_METERS * atan2(sqrt(a), sqrt(1 - a))


def nearest_permits(
    db: Session,
    lat: float,
    lon: float,
    status: Optional[str] = "APPROVED",
) -> list[NearestPermitResponse]:
    """Return up to 5 permits nearest to the given coordinates.

    Starts with a small bounding box and doubles it each iteration until at least
    5 candidates are found or MAX_BOUNDING_BOX_DEGREES is reached. The final
    candidate set is then sorted by exact haversine distance and the top 5 returned.
    """
    box = BOUNDING_BOX_DEGREES
    while True:
        query = db.query(Permit).filter(
            Permit.latitude.isnot(None),
            Permit.longitude.isnot(None),
            Permit.latitude.between(lat - box, lat + box),
            Permit.longitude.between(lon - box, lon + box),
        )
        if status:
            query = query.filter(Permit.status.ilike(status))
        candidates = query.all()
        if len(candidates) >= 5 or box >= MAX_BOUNDING_BOX_DEGREES:
            break
        box = min(box * 2, MAX_BOUNDING_BOX_DEGREES)
    ranked = sorted(candidates, key=lambda p: haversine(lat, lon, p.latitude, p.longitude))

    results = []
    for permit in ranked[:5]:
        data = permit.__dict__.copy()
        data["distance_meters"] = haversine(lat, lon, permit.latitude, permit.longitude)
        results.append(NearestPermitResponse(**data))

    return results
