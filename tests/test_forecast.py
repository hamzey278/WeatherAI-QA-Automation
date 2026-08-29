import pytest
from clients.weather_api_client import WeatherAPIClient
from utils.assertions import assert_json_content_type, assert_status_code


@pytest.mark.forecast
class TestForecastAPI:
    """Tests for GET /v1/forecast endpoint alias."""

    def test_forecast_alias_contract(self, api_client: WeatherAPIClient):
        """Verify GET /v1/forecast delegates to same weather structure as /v1/weather."""
        weather_res = api_client.get_weather(lat=-1.2921, lon=36.8219, days=5)
        forecast_res = api_client.get_forecast(lat=-1.2921, lon=36.8219, days=5)

        assert_status_code(weather_res, 200)
        assert_status_code(forecast_res, 200)
        assert_json_content_type(forecast_res)

        weather_keys = set(weather_res.json().keys())
        forecast_keys = set(forecast_res.json().keys())
        assert forecast_keys == weather_keys, f"Alias /v1/forecast top-level keys {forecast_keys} differ from /v1/weather keys {weather_keys}"
