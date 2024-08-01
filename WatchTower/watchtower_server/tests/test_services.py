from api.services import insert_data, fetch_data
from api.schemas import DataResponse

def test_insert_data():
    data = DataResponse(key="test_key", value="test_value")
    assert insert_data(data) is True

def test_fetch_data():
    data = fetch_data("test_key")
    assert data == {"key": "test_key", "value": "test_value"}
