import requests
import pytest

# Base URL fixture pointing to the running server
@pytest.fixture
def base_url():
    return "http://localhost:5000" 

def test_get_interactions_per_product_valid(base_url):
    """
    Test case to validate that the interactions per product can be retrieved
    from a running database with real data.
    """
    response = requests.get(f"{base_url}/api/v1/interactions/products")
    
    assert response.status_code == 200
    data = response.json()

    assert len(data["data"]) > 0
    assert data["data"][0]["customer_type"] in ["Red", "Orange", "Blue"]
    assert "products" in data["data"][0]
    assert len(data["data"][0]["products"]) > 0
    assert "product" in data["data"][0]["products"][0]
    assert data["data"][0]["products"][0]["product"] == "Sand"
    assert "interaction_count" in data["data"][0]["products"][0]
    assert data["data"][0]["products"][0]["interaction_count"] > 0
