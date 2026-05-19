import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_admin_token():
    response = client.post("/auth/login", data={
        "username": "admin@test.com",
        "password": "admin123"
    })
    assert response.status_code == 200, "Admin login failed"
    return response.json()["access_token"]


def get_pending_mentor_id(token: str) -> int:
    response = client.get(
        "/api/v1/admin/mentor-applications",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0, "Nema mentorica na čekanju — pokreni seed.py"
    return data[0]["id"]


# --- GET testovi (Task 1) ---

def test_get_pending_applications_unauthorized():
    response = client.get("/api/v1/admin/mentor-applications")
    assert response.status_code == 401


def test_get_pending_applications_as_admin():
    token = get_admin_token()
    response = client.get(
        "/api/v1/admin/mentor-applications",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert item["is_approved"] == False


def test_get_pending_applications_pagination():
    token = get_admin_token()
    response = client.get(
        "/api/v1/admin/mentor-applications?skip=0&limit=2",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) <= 2


# --- PATCH approve testovi (Task 2) ---

def test_approve_mentor_unauthorized():
    response = client.patch("/api/v1/admin/mentor-applications/1/approve")
    assert response.status_code == 401


def test_approve_mentor_success():
    token = get_admin_token()
    mentor_id = get_pending_mentor_id(token)

    response = client.patch(
        f"/api/v1/admin/mentor-applications/{mentor_id}/approve",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_approved"] == True
    assert data["id"] == mentor_id


def test_approved_mentor_visible_on_public_list():
    token = get_admin_token()
    mentor_id = get_pending_mentor_id(token)

    # Odobri mentoricu
    client.patch(
        f"/api/v1/admin/mentor-applications/{mentor_id}/approve",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Provjeri da se pojavljuje na javnoj listi
    response = client.get("/mentoring/mentors")
    assert response.status_code == 200
    ids = [m["id"] for m in response.json()]
    assert mentor_id in ids


def test_approve_mentor_not_found():
    token = get_admin_token()
    response = client.patch(
        "/api/v1/admin/mentor-applications/99999/approve",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


# --- PATCH reject testovi (Task 2) ---

def test_reject_mentor_unauthorized():
    response = client.patch("/api/v1/admin/mentor-applications/1/reject")
    assert response.status_code == 401


def test_reject_mentor_success():
    token = get_admin_token()

    all_mentors = client.get(
        "/api/v1/admin/mentor-applications?limit=100",
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    if not all_mentors:
        pytest.skip("Nema mentorica u bazi — pokreni seed.py")

    mentor_id = all_mentors[0]["id"]

    response = client.patch(
        f"/api/v1/admin/mentor-applications/{mentor_id}/reject",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_approved"] == False
    assert data["id"] == mentor_id


def test_reject_mentor_not_found():
    token = get_admin_token()
    response = client.patch(
        "/api/v1/admin/mentor-applications/99999/reject",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


# --- DELETE testovi (Task 13) ---

def test_delete_mentor_unauthorized():
    response = client.delete("/api/v1/admin/mentor-applications/1")
    assert response.status_code == 401


def test_delete_mentor_success():
    token = get_admin_token()

    # Kreiraj mentoricu direktno za ovaj test
    from app.database import SessionLocal
    from app.models.mentor import Mentor, ApplicationStatus
    db = SessionLocal()
    mentor = Mentor(first_name="Test", last_name="Brisanje", email="brisanje@test.com", field_of_expertise="Test", status=ApplicationStatus.APPROVED, is_approved=True)
    db.add(mentor)
    db.commit()
    db.refresh(mentor)
    mentor_id = mentor.id
    db.close()

    response = client.delete(
        f"/api/v1/admin/mentor-applications/{mentor_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_delete_mentor_not_found():
    token = get_admin_token()
    response = client.delete(
        "/api/v1/admin/mentor-applications/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404