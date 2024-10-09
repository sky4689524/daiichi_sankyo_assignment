import pytest
from flask import Flask
from src.controllers.interactions_controller import interactions_blueprint

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
    Sets up the Flask app with the interactions blueprint and test database configuration.
    """
    app = Flask(__name__)
    app.config.update(test_config)
    app.register_blueprint(interactions_blueprint)
    return app


@pytest.fixture
def client(app):
    """
    Provides a test client for interacting with the Flask app.
    """
    return app.test_client()


def test_get_customer_interactions_valid(client, mocker):
    """
    Test case to validate interaction retrieval for an existing customer (ID = 1)
    using a mocked database connection.
    """
    mock_db = mocker.patch('src.controllers.interactions_controller.get_db_connection')
    mock_cursor = mocker.Mock()
    mock_db.return_value.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {"Customer_Id": 1}
    mock_cursor.fetchall.return_value = [
        {"event": "Email", "count": 5},
        {"event": "Call", "count": 2}
    ]

    response = client.get("/api/v1/interactions/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["data"]["customer_id"] == 1
    assert data["data"]["interactions"]["Email"] == 5
    assert data["data"]["interactions"]["Call"] == 2
    assert data["data"]["interactions"]["Bird"] == 0


def test_get_customer_interactions_not_found(client, mocker):
    """
    Test case to handle the scenario when a customer does not exist (ID = 999)
    using a mocked database connection.
    """
    mock_db = mocker.patch('src.controllers.interactions_controller.get_db_connection')
    mock_cursor = mocker.Mock()
    mock_db.return_value.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    response = client.get("/api/v1/interactions/999")
    
    assert response.status_code == 404
    assert "error" in response.get_json()
    assert response.get_json()["error"] == "Customer with id 999 not found"
