import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.models.orm import Permit
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

    # Permits clustered around SF City Hall (37.7793, -122.4193)
    # Each ~1km further away than the last
    session.add_all([
        Permit(locationid=1, applicant="Truck A", status="APPROVED", address="1 ST", latitude=37.7793, longitude=-122.4193),
        Permit(locationid=2, applicant="Truck B", status="APPROVED", address="2 ST", latitude=37.7883, longitude=-122.4193),
        Permit(locationid=3, applicant="Truck C", status="APPROVED", address="3 ST", latitude=37.7973, longitude=-122.4193),
        Permit(locationid=4, applicant="Truck D", status="APPROVED", address="4 ST", latitude=37.8063, longitude=-122.4193),
        Permit(locationid=5, applicant="Truck E", status="APPROVED", address="5 ST", latitude=37.8153, longitude=-122.4193),
        Permit(locationid=6, applicant="Truck F", status="APPROVED", address="6 ST", latitude=37.8243, longitude=-122.4193),
        Permit(locationid=7, applicant="Truck G", status="EXPIRED",  address="7 ST", latitude=37.7800, longitude=-122.4193),
        Permit(locationid=8, applicant="Truck H", status="APPROVED", address="8 ST", latitude=None,   longitude=None),
    ])
    session.commit()

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    session.close()


def test_returns_5_nearest(client):
    response = client.get("/permits/nearest?lat=37.7793&lon=-122.4193")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 5


def test_results_sorted_by_distance(client):
    response = client.get("/permits/nearest?lat=37.7793&lon=-122.4193")
    distances = [r["distance_meters"] for r in response.json()]
    assert distances == sorted(distances)


def test_default_status_is_approved(client):
    response = client.get("/permits/nearest?lat=37.7793&lon=-122.4193")
    assert all(r["status"] == "APPROVED" for r in response.json())


def test_all_statuses_when_status_empty(client):
    response = client.get("/permits/nearest?lat=37.7793&lon=-122.4193&status=")
    assert response.status_code == 200
    statuses = {r["status"] for r in response.json()}
    assert "EXPIRED" in statuses


def test_excludes_null_coordinates(client):
    response = client.get("/permits/nearest?lat=37.7793&lon=-122.4193&status=")
    ids = [r["locationid"] for r in response.json()]
    assert 8 not in ids  # Truck H has no coordinates


def test_fewer_than_5_when_not_enough_matches(client):
    # Search far away — only trucks within bounding box (~11km) are considered
    response = client.get("/permits/nearest?lat=40.0&lon=-74.0")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_missing_lat_returns_422(client):
    response = client.get("/permits/nearest?lon=-122.4193")
    assert response.status_code == 422


def test_missing_lon_returns_422(client):
    response = client.get("/permits/nearest?lat=37.7793")
    assert response.status_code == 422
