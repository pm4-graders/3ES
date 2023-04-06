from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_router_scanner_save():
    response = client.post("/scan/save")
    assert response.status_code == 200
