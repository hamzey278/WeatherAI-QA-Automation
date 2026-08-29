import pytest
from clients.weather_api_client import WeatherAPIClient
from utils.assertions import assert_json_content_type, assert_required_fields, assert_status_code


@pytest.mark.geo
class TestWeatherGeoAPI:
    """Tests for GET /v1/weather-geo and GET /v1/ip-lookup endpoints."""

    def test_ip_lookup_auto(self, api_client: WeatherAPIClient):
        """Verify GET /v1/ip-lookup with ip=auto parameter."""
        response = api_client.get_ip_lookup(ip="auto")
        assert_status_code(response, 200)
        assert_json_content_type(response)
        data = response.json()
        assert_required_fields(data, ["ip", "geo"])
        geo = data["geo"]
        assert_required_fields(geo, ["lat", "lon"])

    def test_ip_lookup_explicit_ipv4(self, api_client: WeatherAPIClient):
        """Verify GET /v1/ip-lookup with explicit IPv4 address."""
        ip = "41.90.64.1"
        response = api_client.get_ip_lookup(ip=ip)
        assert_status_code(response, 200)
        data = response.json()
        assert data.get("ip") == ip

    def test_weather_geo_auto(self, api_client: WeatherAPIClient):
        """Verify GET /v1/weather-geo auto-detects caller location."""
        response = api_client.get_weather_geo(ip="auto")
        assert_status_code(response, 200)
        data = response.json()
        assert "location" in data or "current" in data
