import pytest
from clients.weather_api_client import WeatherAPIClient
from config.test_data import (
    AI_TEST_CASES,
    DAYS_TEST_CASES,
    INVALID_LATITUDES,
    INVALID_LONGITUDES,
    LANGUAGE_TEST_CASES,
    UNITS_TEST_CASES,
)
from utils.assertions import assert_error_response, assert_status_code


@pytest.mark.error
class TestErrorHandlingAndEdgeCases:
    """Boundary, edge-case, and negative test suite for WeatherAI API."""

    @pytest.mark.parametrize("tc", INVALID_LATITUDES, ids=lambda tc: tc["reason"])
    def test_invalid_latitude_parameters(self, api_client: WeatherAPIClient, tc: dict):
        """Verify 400 Bad Request for out-of-range or malformed latitude values."""
        response = api_client.get_weather(lat=tc["lat"], lon=36.8219)
        assert response.status_code != 500, f"Server returned 500 Internal Error for invalid lat {tc['lat']}"
        assert_error_response(response, tc["expected_status"])

    @pytest.mark.parametrize("tc", INVALID_LONGITUDES, ids=lambda tc: tc["reason"])
    def test_invalid_longitude_parameters(self, api_client: WeatherAPIClient, tc: dict):
        """Verify 400 Bad Request for out-of-range or malformed longitude values."""
        response = api_client.get_weather(lat=-1.2921, lon=tc["lon"])
        assert response.status_code != 500, f"Server returned 500 Internal Error for invalid lon {tc['lon']}"
        assert_error_response(response, tc["expected_status"])

    @pytest.mark.parametrize("tc", [t for t in DAYS_TEST_CASES if not t["valid"]], ids=lambda tc: tc["description"])
    def test_invalid_days_parameters(self, api_client: WeatherAPIClient, tc: dict):
        """Verify 400 Bad Request for zero, negative, out-of-bounds, or non-integer days values."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, days=tc["days"])
        assert response.status_code != 500, f"Server returned 500 Internal Error for invalid days {tc['days']}"
        assert_error_response(response, tc["expected_status"])

    @pytest.mark.parametrize("tc", [t for t in UNITS_TEST_CASES if not t["valid"]], ids=lambda tc: f"units_{tc['units']}")
    def test_invalid_units_parameter(self, api_client: WeatherAPIClient, tc: dict):
        """Verify 400 Bad Request for unsupported units parameter values."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, units=tc["units"])
        assert response.status_code != 500, f"Server returned 500 Internal Error for invalid units {tc['units']}"
        assert_error_response(response, tc["expected_status"])

    @pytest.mark.parametrize("tc", [t for t in LANGUAGE_TEST_CASES if not t["valid"]], ids=lambda tc: f"lang_{tc['lang']}")
    def test_invalid_language_parameter(self, api_client: WeatherAPIClient, tc: dict):
        """Verify 400 Bad Request for unsupported language parameter values."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, lang=tc["lang"])
        assert response.status_code != 500, f"Server returned 500 Internal Error for invalid lang {tc['lang']}"
        assert_error_response(response, tc["expected_status"])

    @pytest.mark.parametrize("tc", [t for t in AI_TEST_CASES if not t["valid"]], ids=lambda tc: f"ai_{tc['ai']}")
    def test_invalid_ai_parameter(self, api_client: WeatherAPIClient, tc: dict):
        """Verify 400 Bad Request for invalid boolean string in AI parameter."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, ai=tc["ai"])
        assert response.status_code != 500, f"Server returned 500 Internal Error for invalid ai {tc['ai']}"
        assert_error_response(response, tc["expected_status"])

    @pytest.mark.skip(reason="Plan-restricted endpoint; tested via contract assertions to avoid consuming SMS quota.")
    def test_sms_api_plan_restriction_403(self, api_client: WeatherAPIClient):
        """Documented manual test: SMS API endpoints return 403 SMS_NOT_ENABLED on non-Scale plans."""
        pass

    @pytest.mark.skip(reason="Rate-limiting (429) test skipped to protect monthly API quota; rate headers validated instead.")
    def test_rate_limit_exceeded_429(self, api_client: WeatherAPIClient):
        """Documented manual test: Rapid excessive requests should trigger 429 Too Many Requests."""
        pass
