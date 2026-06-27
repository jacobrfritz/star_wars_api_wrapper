import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.star_wars_api_wrapper.api.v1.endpoints.people import router

# Setup local app for testing
app = FastAPI()
app.include_router(router)
client = TestClient(app)


# --- Mock Data Factory ---
def get_mock_swapi_data(height="172", mass="77"):
    """Returns a valid SWAPI JSON structure with variable height/mass."""
    return {
        "name": "Luke Skywalker",
        "height": height,
        "mass": mass,
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
        "homeworld": "https://swapi.info/api/planets/1",
        "films": ["https://swapi.info/api/films/1"],
        "species": [],
        "vehicles": [],
        "starships": [],
        "created": "2014-12-09T13:50:51.644000Z",
        "edited": "2014-12-20T21:17:56.891000Z",
        "url": "https://swapi.info/api/people/1",
    }


# --- Tests ---


def test_successful_mapping_and_coercion(mocker):
    """Test that a valid SWAPI response maps and coerces strings to ints."""
    mock_data = get_mock_swapi_data(height="172", mass="77")

    # Mock the external SWAPI call using pytest-mock
    # This intercepts the AsyncClient.get inside your endpoint
    mock_response = httpx.Response(200, json=mock_data)
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    response = client.get("/people/1")

    assert response.status_code == 200

    data = response.json()
    # Assert that coercion successfully turned strings into integers
    assert data["height"] == 172
    assert data["mass"] == 77
    assert data["name"] == "Luke Skywalker"


def test_coercion_with_dirty_strings(mocker):
    """Test that coercion strips away non-numeric characters (e.g. '77kg')."""
    mock_data = get_mock_swapi_data(height="172cm", mass="77kg")

    mock_response = httpx.Response(200, json=mock_data)
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    response = client.get("/people/1")

    assert response.status_code == 200
    data = response.json()
    assert data["height"] == 172
    assert data["mass"] == 77


def test_unrecognized_number(mocker):
    """Test that coercion return None for integer types that aren't numbers"""
    mock_data = get_mock_swapi_data(height="unknown", mass="unknown")

    mock_response = httpx.Response(200, json=mock_data)
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    response = client.get("/people/1")

    assert response.status_code == 200
    data = response.json()
    assert data["height"] is None
    assert data["mass"] is None


def test_swapi_returns_error(mocker):
    """Test that your endpoint forwards the error if SWAPI fails."""
    mock_response = httpx.Response(404, text="Not Found")
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    response = client.get("/people/999")

    assert response.status_code == 404
    assert "Swapi returned an error" in response.json()["detail"]
