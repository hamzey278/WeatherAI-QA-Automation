import pytest
from clients.weather_api_client import WeatherAPIClient
from utils.assertions import assert_json_content_type, assert_status_code


@pytest.mark.hourly
class TestHourlyWeatherAPI:
    """Tests for GET /v1/hourly endpoint."""

    def test_hourly_weather_forecast(self, api_client: WeatherAPIClient):
        """Verify GET /v1/hourly returns valid hourly weather data."""
        response = api_client.get_hourly(lat=-1.2921, lon=36.8219)
        assert_status_code(response, 200)
        assert_json_content_type(response)
        data = response.json()
        assert "location" in data or "current" in data
