import pytest
from clients.weather_api_client import WeatherAPIClient
from config.test_data import VALID_COORDINATES
from utils.assertions import (
    assert_json_content_type,
    assert_rate_limit_headers,
    assert_required_fields,
    assert_status_code,
    assert_valid_coordinates,
)


@pytest.mark.weather
class TestWeatherAPI:
    """Happy path and parameter functional tests for GET /v1/weather endpoint."""

    @pytest.mark.parametrize("location", VALID_COORDINATES, ids=lambda loc: loc["name"])
    def test_get_weather_valid_coordinates(self, api_client: WeatherAPIClient, location: dict):
        """Verify successful weather response for diverse valid global geographic coordinates."""
        response = api_client.get_weather(lat=location["lat"], lon=location["lon"])
        assert_status_code(response, 200)
        assert_json_content_type(response)
        assert_rate_limit_headers(response)

        data = response.json()
        assert_required_fields(data, ["location", "units", "current", "forecast"])

        # Validate location invariants
        loc_data = data["location"]
        assert_valid_coordinates(loc_data["lat"], loc_data["lon"])
        assert abs(loc_data["lat"] - location["lat"]) < 0.5, f"Returned latitude {loc_data['lat']} differs from requested {location['lat']}"
        assert abs(loc_data["lon"] - location["lon"]) < 0.5, f"Returned longitude {loc_data['lon']} differs from requested {location['lon']}"

        # Validate current condition types
        current = data["current"]
        assert isinstance(current["temperature"], (int, float)), "Current temperature must be numeric"
        assert current["temperature"] is not None, "Current temperature cannot be null"

    @pytest.mark.parametrize("days", [1, 3, 7, 14])
    def test_forecast_days_length(self, api_client: WeatherAPIClient, days: int):
        """Verify forecast array length matches requested days parameter."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, days=days)
        assert_status_code(response, 200)
        data = response.json()
        assert "forecast" in data
        assert len(data["forecast"]) == days, f"Requested {days} forecast days, but received {len(data['forecast'])}"

    def test_ai_summary_enabled(self, api_client: WeatherAPIClient):
        """Verify AI summary field presence when ai parameter is true."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, ai=True)
        assert_status_code(response, 200)
        data = response.json()
        assert "ai_summary" in data
        assert data["ai_summary"] is not None and len(data["ai_summary"]) > 0

    def test_ai_summary_disabled(self, api_client: WeatherAPIClient):
        """Verify weather response when ai parameter is set to false."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, ai=False)
        assert_status_code(response, 200)
        data = response.json()
        # When ai=false, ai_summary should be omitted or null
        assert data.get("ai_summary") is None or "ai_summary" not in data

    @pytest.mark.parametrize("units,expected_temp_unit", [("metric", "C"), ("imperial", "F")])
    def test_units_parameter(self, api_client: WeatherAPIClient, units: str, expected_temp_unit: str):
        """Verify metric and imperial unit conversions in weather metadata."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, units=units)
        assert_status_code(response, 200)
        data = response.json()
        assert "units" in data
        assert data["units"]["temperature"] == expected_temp_unit

    @pytest.mark.parametrize("lang", ["en", "sw"])
    def test_supported_languages(self, api_client: WeatherAPIClient, lang: str):
        """Verify localization response for supported languages (English and Swahili)."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, lang=lang)
        assert_status_code(response, 200)
        data = response.json()
        assert data.get("language") == lang
