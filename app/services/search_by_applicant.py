from typing import Optional
from sqlalchemy.orm import Session
from app.models.orm import Permit

def search_by_applicant(
    db: Session,
    applicant: str,
    status: Optional[str] = None,
    limit: int = 100,
) -> list[Permit]:
    """Return permits matching the given applicant name (case-insensitive), optionally filtered by status."""
    query = db.query(Permit).filter(Permit.applicant.ilike(applicant))
    if status:
        query = query.filter(Permit.status.ilike(status))
    return query.limit(limit).all()
