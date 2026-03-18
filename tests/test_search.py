import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models import Permit
from app.main import app

@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add_all([
        Permit(locationid=1, applicant="Sanchez Tacos", status="APPROVED", address="100 SANSOME ST"),
        Permit(locationid=2, applicant="Sanchez Burritos", status="EXPIRED", address="200 MARKET ST"),
        Permit(locationid=3, applicant="Hot Dog Stand", status="APPROVED", address="300 SANSOME ST"),
    ])
    session.commit()

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    session.close()


def test_search_by_applicant_exact_match(client):
    response = client.get("/permits/search?applicant=Sanchez Tacos")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["applicant"] == "Sanchez Tacos"


def test_search_by_applicant_partial_returns_nothing(client):
    response = client.get("/permits/search?applicant=sanchez")
    assert response.status_code == 200
    assert response.json() == []


def test_search_by_applicant_and_status(client):
    response = client.get("/permits/search?applicant=Sanchez Tacos&status=APPROVED")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["status"] == "APPROVED"


def test_search_by_address_partial_match(client):
    response = client.get("/permits/search?address=SAN")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    assert all("SANSOME" in r["address"] for r in results)


def test_search_no_params_returns_400(client):
    response = client.get("/permits/search")
    assert response.status_code == 400


def test_search_no_match_returns_empty(client):
    response = client.get("/permits/search?address=xyz")
    assert response.status_code == 200
    assert response.json() == []
