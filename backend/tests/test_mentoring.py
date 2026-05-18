import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from app.models.mentor import Mentor  

from app.main import app
from app.database import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_backend.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Pošto je Mentor importovan na samom vrhu, create_all će SIGURNO napraviti 'mentors' tabelu
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Brišemo je nakon testa da sljedeći test krene od nule
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass
  
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()



def test_get_mentor_success(client: TestClient, db_session: sessionmaker):
  
    test_mentor = Mentor(
        id=1,
        first_name="Amina",
        last_name="Valic",
        email="amina.valic@example.com",
        field_of_expertise="Data, AI i digitalna transformacija",
        preferred_session_format="Online",
        max_mentees=1
    )
    db_session.add(test_mentor)
    db_session.commit()
    
   
    response = client.get("/mentoring/mentors/1")
    assert response.status_code == 200

def test_get_mentor_not_found(client: TestClient):
    response = client.get("/mentoring/mentors/9999")
    assert response.status_code == 404