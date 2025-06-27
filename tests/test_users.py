from fastapi.testclient import TestClient
from app.main import app
from tests.test_database import TestingSessionLocal
from app.database import get_db

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#override_get_db.__name__ = "override_get_db"
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"name": "TestUser", "age": 99, "birth_state": "ZZ"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestUser"
    assert data["age"] == 99
    assert data["birth_state"] == "ZZ"
    assert "id" in data

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_update_user():
    # Create a new user first
    response = client.post("/users/", json={"name": "UpdateMe", "age": 20, "birth_state": "AA"})
    user_id = response.json()["id"]

    # Now update
    response = client.put(f"/users/{user_id}", json={"name": "Updated", "age": 21, "birth_state": "BB"})
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == "Updated"
    assert updated_user["age"] == 21
    assert updated_user["birth_state"] == "BB"

def test_delete_user():
    # Create a new user to delete
    response = client.post("/users/", json={"name": "ToDelete", "age": 33, "birth_state": "CC"})
    user_id = response.json()["id"]

    # Delete them
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    # Confirm they're gone
    response = client.get("/users/")
    ids = [u["id"] for u in response.json()]
    assert user_id not in ids
