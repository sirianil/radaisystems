from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
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
