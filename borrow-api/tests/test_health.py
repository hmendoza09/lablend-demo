from app import app


def test_health_returns_200():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["service"] == "borrow-api"
