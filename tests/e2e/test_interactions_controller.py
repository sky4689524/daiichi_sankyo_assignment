import requests
import pytest

# Base URL fixture pointing to the running server
@pytest.fixture
def base_url():
    return "http://localhost:5000" 

def test_get_customer_interactions_valid(base_url):
    """
    Test case to validate a successful interaction retrieval for an existing customer (ID = 1).
    """
    response = requests.get(f"{base_url}/api/v1/interactions/1")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "customer_id" in data["data"]
    assert data["data"]["customer_id"] == 1
    assert data["data"]["interactions"]["Email"] >= 0
    assert data["data"]["interactions"]["Call"] >= 0
    assert data["data"]["interactions"]["Bird"] >= 0


def test_get_customer_interactions_not_found(base_url):
    """
    Test case to handle customer not found scenario (ID = 999).
    """
    response = requests.get(f"{base_url}/api/v1/interactions/999")
    
    assert response.status_code == 404
    data = response.json()
    
    assert "error" in data
    assert data["error"] == "Customer with id 999 not found"
