from contextlib import asynccontextmanager
from math import radians, sin, cos, sqrt, atan2
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Permit, PermitResponse, NearestPermitResponse
from app.seed import seed

EARTH_RADIUS_METERS = 6_371_000
BOUNDING_BOX_DEGREES = 0.1  # ~11km

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_METERS * atan2(sqrt(a), sqrt(1 - a))

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=FileResponse)
def index():
    return "static/index.html"

@app.get("/permits/search", response_model=list[PermitResponse])
def search_permits(
    applicant: Optional[str] = None,
    address: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if applicant:
        query = db.query(Permit).filter(Permit.applicant.ilike(applicant))
        if status:
            query = query.filter(Permit.status.ilike(status))
        return query.all()
    if address:
        return db.query(Permit).filter(Permit.address.ilike(f"%{address}%")).all()
    raise HTTPException(status_code=400, detail="Provide either 'applicant' or 'address'")

@app.get("/permits/nearest", response_model=list[NearestPermitResponse])
def nearest_permits(
    lat: float,
    lon: float,
    status: Optional[str] = "APPROVED",
    db: Session = Depends(get_db),
):
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
