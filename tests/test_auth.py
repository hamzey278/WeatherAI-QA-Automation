import pytest
from clients.weather_api_client import WeatherAPIClient
from utils.assertions import assert_error_response, assert_json_content_type, assert_status_code


@pytest.mark.auth
class TestAuthentication:
    """Test suite covering WeatherAI API authentication and authorization mechanisms."""

    def test_valid_api_key(self, api_client: WeatherAPIClient):
        """Verify successful response with valid Bearer token authentication."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, raw_auth_header="Bearer wai_valid_sample_key_12345")
        assert_status_code(response, 200)
        assert_json_content_type(response)
        data = response.json()
        assert "location" in data or "current" in data

    def test_missing_authorization_header(self, api_client: WeatherAPIClient):
        """Verify 401 Unauthorized response when Authorization header is omitted."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, raw_auth_header="")
        assert_error_response(response, 401)

    def test_invalid_api_key(self, api_client: WeatherAPIClient):
        """Verify 401 Unauthorized response when an invalid Bearer token is provided."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, raw_auth_header="Bearer wai_invalid_key_999999")
        data = assert_error_response(response, 401)
        # Ensure secret token is not leaked back in the error message
        response_text = response.text.lower()
        assert "wai_invalid_key_999999" not in response_text, "Sensitive API key leaked in error response body!"

    def test_malformed_authorization_header(self, api_client: WeatherAPIClient):
        """Verify 401 Unauthorized response when Authorization header format is malformed (e.g. Basic instead of Bearer)."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, raw_auth_header="Basic wai_sample_token")
        assert_error_response(response, 401)

    def test_empty_bearer_token(self, api_client: WeatherAPIClient):
        """Verify 401 Unauthorized response when Bearer prefix is supplied without a token string."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, raw_auth_header="Bearer ")
        assert_error_response(response, 401)
