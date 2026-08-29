import pytest
from clients.weather_api_client import WeatherAPIClient
from utils.assertions import assert_json_content_type, assert_status_code, assert_valid_coordinates


@pytest.mark.current
class TestCurrentWeatherAPI:
    """Tests for GET /v1/current endpoint."""

    def test_get_current_weather_success(self, api_client: WeatherAPIClient):
        """Verify successful response from GET /v1/current for valid coordinates."""
        response = api_client.get_current(lat=-1.2921, lon=36.8219)
        assert_status_code(response, 200)
        assert_json_content_type(response)
        data = response.json()

        assert "location" in data or "current" in data
        current = data.get("current", data)
        assert "temperature" in current
        assert isinstance(current["temperature"], (int, float))

    @pytest.mark.parametrize("units", ["metric", "imperial"])
    def test_get_current_weather_units(self, api_client: WeatherAPIClient, units: str):
        """Verify GET /v1/current with units parameter."""
        response = api_client.get_current(lat=35.6762, lon=139.6503, units=units)
        assert_status_code(response, 200)
        data = response.json()
        assert "units" in data
