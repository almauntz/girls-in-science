from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import pytest

from app.main import app
from app.database import get_db
from app.models.mentor import Mentor


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_get_mentors_empty(client: TestClient):
    response = client.get("/mentoring/mentors")
    assert response.status_code == 200
    assert response.json() == []


def test_get_mentors_returns_only_approved(client: TestClient, session: Session):
    session.add(Mentor(
        first_name="Odobrena", last_name="Test",
        email="odobrena@test.com", field_of_expertise="IT",
        is_approved=True
    ))
    session.add(Mentor(
        first_name="Neodobrena", last_name="Test",
        email="neodobrena@test.com", field_of_expertise="IT",
        is_approved=False
    ))
    session.commit()

    response = client.get("/mentoring/mentors")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["first_name"] == "Odobrena"


def test_get_mentors_pagination(client: TestClient, session: Session):
    for i in range(5):
        session.add(Mentor(
            first_name=f"Mentor{i}", last_name="Test",
            email=f"mentor{i}@test.com", field_of_expertise="IT",
            is_approved=True
        ))
    session.commit()

    response = client.get("/mentoring/mentors?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2