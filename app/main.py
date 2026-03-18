from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Permit, PermitResponse
from app.seed import seed

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

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
