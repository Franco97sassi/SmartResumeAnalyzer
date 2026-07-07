from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_swagger():

    response = client.get("/docs")

    assert response.status_code == 200


def test_analyze():

    response = client.post(
        "/api/analyze",
        json={
            "text": "Tengo experiencia con Python y FastAPI."
        }
    )

    assert response.status_code == 200

    assert "analysis" in response.json()