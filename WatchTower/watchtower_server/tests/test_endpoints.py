from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_receive_data():
    response = client.post("/data", json={"key": "test_key", "value": "test_value"})
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

def test_get_data():
    response = client.get("/data/test_key")
    assert response.status_code == 200
    assert response.json() == {"key": "test_key", "value": "test_value"}
