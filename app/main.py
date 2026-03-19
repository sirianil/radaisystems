# Entry point for the FastAPI application.
# On startup, creates database tables and seeds permit data from CSV.

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.db.session import engine, Base
from app.db.seed import seed
from app.api.permits import router as permits_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables defined in ORM models, then seed from CSV if empty.
    Base.metadata.create_all(bind=engine)
    seed()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
# mounts API routes under /permits.
app.include_router(permits_router)

# Serves the static frontend at /
@app.get("/", response_class=FileResponse)
def index():
    return "static/index.html"
