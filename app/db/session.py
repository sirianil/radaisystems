# Database session setup using SQLAlchemy.
# DATABASE_URL points to a SQLite file inside the Docker container at /code/permits.db.
# get_db() is a FastAPI dependency that yields a session and ensures it is closed afterward.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:////code/permits.db"

# check_same_thread=False is required for SQLite when used with FastAPI's async request handling.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
