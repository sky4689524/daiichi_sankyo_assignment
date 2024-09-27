import pytest
from flask import Flask
from src.controllers.statistics_controller import stats_blueprint
from src.factory import get_statistics_repository


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
    Sets up the Flask app with the stats blueprint and the test configuration.
    """
    app = Flask(__name__)
    app.config.update(test_config)
    app.register_blueprint(stats_blueprint)
    return app

@pytest.fixture
def client(app):
    """
    Provides a test client for interacting with the Flask app.
    """
    return app.test_client()

def test_get_wrong_table(client, mocker):
    """
    Test case to check the behavior when querying a non-existent table 
    using a mocked database repository.
    """
    mock_repo = mocker.patch('src.factory.get_statistics_repository')
    mock_repo.return_value.check_table_name.return_value = False

    response = client.get('/api/v1/stats/wrong_table')
    assert response.status_code == 404, f"Response text: {response.data.decode()}"
    assert "message" in response.get_json()
    assert response.get_json()["message"] == "Table name not found"

def test_number_of_customers(client, mocker):
    """
    Test case to verify the number of rows in the 'customers' table 
    using a mocked database repository.
    """
    mock_repo = mocker.patch('src.factory.get_statistics_repository')
    mock_repo.return_value.check_table_name.return_value = True
    mock_repo.return_value.get_number_of_rows.return_value = 10

    response = client.get('/api/v1/stats/customers')
    assert response.status_code == 200, f"Response text: {response.data.decode()}"
    assert "rows" in response.get_json()
    assert response.get_json()["rows"] > 0
