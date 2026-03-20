from sqlalchemy.orm import Session
from app.models.orm import Permit

def search_by_address(db: Session, address: str, limit: int = 100) -> list[Permit]:
    """Return all permits whose address starts with the given string (case-insensitive)."""
    return db.query(Permit).filter(Permit.address.ilike(f"%{address}%")).limit(limit).all()
