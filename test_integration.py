import pytest
from fastapi.testclient import TestClient
from main import app



client = TestClient(app)

# @pytest.fixture
# def client():
#     """Create a TestClient for making requests"""
#     with TestClient(app) as client:
#         yield client


# Test home route
def test_home():
    response = client.get("/")
    assert response.status_code == 200, 'Failed to load the home page'

# Test predict page route
def test_predict_page():
    response = client.get("/predict")
    assert response.status_code == 200, 'Failed to load the predict page'

def test_predict_variety():
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", data=payload)
    assert response.status_code == 200, 'Failed to predict'
    assert "prediction" in response.json(), 'Response missing prediction field'

# pour tester :
# pytest test_integration.py