from app import app


def test_health_returns_200():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_create_item_rejects_invalid_input():
    # Validation fails before the database is touched, so no DB is needed here.
    client = app.test_client()
    response = client.post("/", json={"name": ""})
    assert response.status_code == 400
