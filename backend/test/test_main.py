from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_router_scanner_save():
    response = client.post("/scanner/save")
    assert response.status_code == 200