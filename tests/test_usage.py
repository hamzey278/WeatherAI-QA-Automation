import pytest
from clients.weather_api_client import WeatherAPIClient
from utils.assertions import assert_error_response, assert_json_content_type, assert_required_fields, assert_status_code


@pytest.mark.usage
class TestUsageAPI:
    """Tests for GET /v1/usage endpoint covering quota, request counts, and plan details."""

    def test_get_usage_success(self, api_client: WeatherAPIClient):
        """Verify successful response for GET /v1/usage with valid authentication."""
        response = api_client.get_usage()
        assert_status_code(response, 200)
        assert_json_content_type(response)

        data = response.json()
        assert_required_fields(data, ["plan", "requests"])

        # Validate request quota structure & invariant constraints
        reqs = data["requests"]
        assert_required_fields(reqs, ["used", "limit"])
        assert isinstance(reqs["used"], int) and reqs["used"] >= 0
        assert isinstance(reqs["limit"], int) and reqs["limit"] > 0
        if "remaining" in reqs:
            assert isinstance(reqs["remaining"], int) and reqs["remaining"] >= 0
            assert reqs["used"] + reqs["remaining"] <= reqs["limit"] + 10, "Used + remaining requests exceeds total limit!"

        # Validate AI request quota if present
        if "ai_requests" in data:
            ai_reqs = data["ai_requests"]
            assert isinstance(ai_reqs.get("used", 0), int)
            assert isinstance(ai_reqs.get("limit", 0), int)

        # Validate billing period fields if present
        if "billing_period" in data:
            bp = data["billing_period"]
            assert isinstance(bp, dict)

    def test_get_usage_unauthorized(self, api_client: WeatherAPIClient):
        """Verify 401 Unauthorized response when querying usage without API key."""
        response = api_client.get_usage(raw_auth_header="")
        assert_error_response(response, 401)
