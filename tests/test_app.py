from unittest.mock import patch

import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.testing = True
    app_module.users.clear()
    return app_module.app.test_client()


def test_create_user_success(client):
    resp = client.post("/users", json={"name": "Alice"})
    assert resp.status_code == 201
    assert resp.get_json()["name"] == "Alice"
    assert "id" in resp.get_json()


def test_create_user_missing_name(client):
    resp = client.post("/users", json={})
    assert resp.status_code == 400


def test_create_user_rejects_non_string_name(client):
    resp = client.post("/users", json={"name": 123})
    assert resp.status_code == 400


def test_create_user_rejects_blank_name(client):
    resp = client.post("/users", json={"name": "   "})
    assert resp.status_code == 400


def test_get_users_empty(client):
    resp = client.get("/users")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_get_user_not_found(client):
    resp = client.get("/users/does-not-exist")
    assert resp.status_code == 404


def test_full_crud_flow(client):
    created = client.post("/users", json={"name": "Bob"}).get_json()
    user_id = created["id"]

    fetched = client.get(f"/users/{user_id}")
    assert fetched.status_code == 200
    assert fetched.get_json()["name"] == "Bob"

    updated = client.put(f"/users/{user_id}", json={"name": "Bobby"})
    assert updated.status_code == 200
    assert updated.get_json()["name"] == "Bobby"

    deleted = client.delete(f"/users/{user_id}")
    assert deleted.status_code == 200
    assert deleted.get_json()["name"] == "Bobby"

    assert client.get(f"/users/{user_id}").status_code == 404


def test_update_user_not_found(client):
    resp = client.put("/users/does-not-exist", json={"name": "X"})
    assert resp.status_code == 404


def test_delete_user_not_found(client):
    resp = client.delete("/users/does-not-exist")
    assert resp.status_code == 404


def test_routine_404_does_not_invoke_openai(client):
    with patch("debug_decorator._get_client") as spy:
        resp = client.get("/users/does-not-exist")
        assert resp.status_code == 404
        spy.assert_not_called()
