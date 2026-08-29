import pytest
from clients.weather_api_client import WeatherAPIClient
from utils.assertions import assert_schema_valid, assert_status_code
from utils.helpers import load_schema


@pytest.mark.contract
class TestJSONSchemaContracts:
    """Contract validation test suite verifying response JSON schemas against documented specifications."""

    @pytest.fixture(scope="session")
    def weather_schema(self) -> dict:
        return load_schema("weather_schema.json")

    @pytest.fixture(scope="session")
    def usage_schema(self) -> dict:
        return load_schema("usage_schema.json")

    @pytest.fixture(scope="session")
    def error_schema(self) -> dict:
        return load_schema("error_schema.json")

    @pytest.fixture(scope="session")
    def ip_lookup_schema(self) -> dict:
        return load_schema("ip_lookup_schema.json")

    def test_weather_contract(self, api_client: WeatherAPIClient, weather_schema: dict):
        """Validate GET /v1/weather JSON response against JSON Schema."""
        response = api_client.get_weather(lat=-1.2921, lon=36.8219, days=7, units="metric", ai=True)
        assert_status_code(response, 200)
        assert_schema_valid(response.json(), weather_schema)

    def test_usage_contract(self, api_client: WeatherAPIClient, usage_schema: dict):
        """Validate GET /v1/usage JSON response against JSON Schema."""
        response = api_client.get_usage()
        assert_status_code(response, 200)
        assert_schema_valid(response.json(), usage_schema)

    def test_ip_lookup_contract(self, api_client: WeatherAPIClient, ip_lookup_schema: dict):
        """Validate GET /v1/ip-lookup JSON response against JSON Schema."""
        response = api_client.get_ip_lookup(ip="41.90.64.1")
        assert_status_code(response, 200)
        assert_schema_valid(response.json(), ip_lookup_schema)

    def test_error_contract(self, api_client: WeatherAPIClient, error_schema: dict):
        """Validate 401 Unauthorized error response against JSON Schema."""
        response = api_client.get_weather(raw_auth_header="Bearer wai_invalid_key_123")
        assert_status_code(response, 401)
        assert_schema_valid(response.json(), error_schema)
