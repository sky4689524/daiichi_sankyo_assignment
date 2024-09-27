import pytest
from flask import Flask
from src.controllers.products_controller import products_blueprint

@pytest.fixture
def test_config():
    """
    Fixture to provide the test configuration for the database.
    """
    return {
        "DB_NAME": "business",
        "DB_USER": "postgres",
        "DB_HOST": "localhost",
        "DB_PASSWORD": "thepassword",
        "DB_PORT": 5432,
        "TESTING": True,
    }

@pytest.fixture
def app(test_config):
    """
    Sets up the Flask app with the products blueprint and test database configuration.
    """
    app = Flask(__name__)
    app.config.update(test_config)
    app.register_blueprint(products_blueprint)
    return app

@pytest.fixture
def client(app):
    """
    Provides a test client for interacting with the Flask app.
    """
    return app.test_client()


def test_get_interactions_per_product_valid(client, mocker):
    """
    Test case to validate that the interactions per product can be successfully 
    retrieved using a mocked database connection.
    """
    mock_db = mocker.patch('src.controllers.products_controller.get_db_connection')
    mock_cursor = mocker.Mock()
    mock_db.return_value.cursor.return_value = mock_cursor

    # Simulate the result returned from the database query based on real data
    mock_cursor.fetchall.return_value = [
        {"customer_type": "Red", "product": "Sand", "interaction_count": 7},
        {"customer_type": "Orange", "product": "Sand", "interaction_count": 5},
        {"customer_type": "Blue", "product": "Sand", "interaction_count": 4},
    ]

    response = client.get("/api/v1/interactions/products")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["data"]) == 3
    assert data["data"][0]["customer_type"] == "Red"
    assert data["data"][0]["products"][0]["product"] == "Sand"
    assert data["data"][0]["products"][0]["interaction_count"] == 7
    assert data["data"][1]["customer_type"] == "Orange"
    assert data["data"][1]["products"][0]["product"] == "Sand"
    assert data["data"][1]["products"][0]["interaction_count"] == 5
    assert data["data"][2]["customer_type"] == "Blue"
    assert data["data"][2]["products"][0]["product"] == "Sand"
    assert data["data"][2]["products"][0]["interaction_count"] == 4
