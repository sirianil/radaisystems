# API routes for permit search and nearest-permit lookup.
# All routes are prefixed with /permits.

from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.schemas import PermitResponse, NearestPermitResponse
from app.services import permits as permit_service

router = APIRouter(prefix="/permits")

@router.get("/search/applicant", response_model=list[PermitResponse])
def search_by_applicant(
    applicant: str,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return permit_service.search_by_applicant(db, applicant=applicant, status=status)

@router.get("/search/address", response_model=list[PermitResponse])
def search_by_address(
    address: str,
    db: Session = Depends(get_db),
):
    return permit_service.search_by_address(db, address=address)

@router.get("/nearest", response_model=list[NearestPermitResponse])
def nearest_permits(
    lat: float,
    lon: float,
    status: Optional[str] = "APPROVED",
    db: Session = Depends(get_db),
):
    return permit_service.nearest_permits(db, lat=lat, lon=lon, status=status)
