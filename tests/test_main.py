from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
fake_user = {"username": "firstuser", "password": "first_user_password"}


def test_create_task():
    token = get_auth_token()

    task_info = "Test task"

    response = client.post(
        "/tasks/create",
        headers={"Authorization": f"Bearer {token}"},
        json={"datetime_to_do": "2024-12-31T12:00:00", "task_info": task_info},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["task_info"] == task_info
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    return data["id"]


def test_get_task():
    token = get_auth_token()

    task_id = test_create_task()

    response = client.get(
        f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["task_info"] == "Test task"

    datetime_to_do = datetime.fromisoformat(
        data["datetime_to_do"].replace("Z", "+00:00")
    )
    expected_datetime = datetime(2024, 12, 31, 12, 0, tzinfo=timezone.utc)
    assert datetime_to_do == expected_datetime


def test_update_task():
    token = get_auth_token()

    task_id = test_create_task()

    new_datetime_to_do = "2025-01-01T10:00:00"
    new_task_info = "Updated test task"

    response = client.patch(
        f"/tasks/{task_id}/update",
        headers={"Authorization": f"Bearer {token}"},
        json={"datetime_to_do": new_datetime_to_do, "task_info": new_task_info},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["task_info"] == new_task_info
    assert data["datetime_to_do"] == f"{new_datetime_to_do}Z"
    assert data["id"] == task_id


def test_update_task_unauthorized():
    task_id = test_create_task()

    response = client.patch(
        f"/tasks/{task_id}/update",
        json={
            "datetime_to_do": "2025-01-01T10:00:00",
            "task_info": "Unauthorized update",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_tasks_list():
    token = get_auth_token()

    task_id_1 = test_create_task()
    task_id_2 = test_create_task()

    response = client.get("/tasks", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    task_data = data[0]
    assert "id" in task_data
    assert "datetime_to_do" in task_data
    assert "task_info" in task_data
    assert "created_at" in task_data
    assert "updated_at" in task_data


def get_auth_token():
    response = client.post("/login", data=fake_user)
    assert response.status_code == 200
    return response.json()["access_token"]


def test_login():
    response = client.post("/login", data=fake_user)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_tasks_list_with_auth():
    login_response = client.post("/login", data=fake_user)
    token = login_response.json()["access_token"]

    response = client.get("/tasks", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
