import pytest
from clients.weather_api_client import WeatherAPIClient
from utils.assertions import assert_json_content_type, assert_status_code


@pytest.mark.daily
class TestDailyWeatherAPI:
    """Tests for GET /v1/daily endpoint."""

    def test_daily_weather_forecast(self, api_client: WeatherAPIClient):
        """Verify GET /v1/daily returns valid aggregated daily forecast."""
        response = api_client.get_daily(lat=-1.2921, lon=36.8219, days=7)
        assert_status_code(response, 200)
        assert_json_content_type(response)
        data = response.json()
        assert "forecast" in data
        assert len(data["forecast"]) == 7
