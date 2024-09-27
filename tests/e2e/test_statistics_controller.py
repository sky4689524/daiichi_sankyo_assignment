import requests
import pytest

@pytest.fixture
def base_url():
    """
    Fixture to provide the base URL of the running Flask app.
    """
    return "http://localhost:5000"  # Assuming your Flask app runs here during testing

def test_get_wrong_table(base_url):
    """
    Test case to check the behavior when querying a non-existent table.
    """
    response = requests.get(f"{base_url}/api/v1/stats/wrong_table")
    assert response.status_code == 404
    assert response.json()["message"] == "Table name not found"

def test_number_of_customers(base_url):
    """
    Test case to verify the correct number of rows in the 'customers' table.
    """
    response = requests.get(f"{base_url}/api/v1/stats/customers")
    assert response.status_code == 200
    assert response.json()["rows"] > 0
