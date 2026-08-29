import re
import pytest
import requests_mock
from clients.weather_api_client import WeatherAPIClient
from config.settings import settings
from utils.mock_responses import (
    get_mock_error_response,
    get_mock_ip_lookup_response,
    get_mock_usage_response,
    get_mock_weather_response,
    get_mock_webhooks_response,
)


@pytest.fixture(scope="session")
def api_client() -> WeatherAPIClient:
    """Session-scoped fixture providing a configured WeatherAPIClient instance."""
    return WeatherAPIClient()


@pytest.fixture(autouse=True)
def mock_server_adapter(requests_mock: requests_mock.Mocker):
    """Global fixture configuring contract-compliant mock responses for deterministic execution."""
    base = settings.WEATHER_API_BASE_URL.rstrip("/")

    # Custom matcher callback for GET /v1/weather
    def weather_callback(request, context):
        context.headers["Content-Type"] = "application/json"
        auth_header = request.headers.get("Authorization", "")
        if not auth_header or not auth_header.startswith("Bearer wai_") or "invalid" in auth_header:
            context.status_code = 401
            return get_mock_error_response(401, "Invalid or missing API key")

        query = request.qs
        lat_val = query.get("lat", ["-1.2921"])[0]
        lon_val = query.get("lon", ["36.8219"])[0]

        try:
            lat = float(lat_val)
            lon = float(lon_val)
        except ValueError:
            context.status_code = 400
            return get_mock_error_response(400, "Latitude and longitude must be valid numeric values")

        if not (-90.0 <= lat <= 90.0):
            context.status_code = 400
            return get_mock_error_response(400, "Latitude must be between -90 and 90")
        if not (-180.0 <= lon <= 180.0):
            context.status_code = 400
            return get_mock_error_response(400, "Longitude must be between -180 and 180")

        days_val = query.get("days", ["7"])[0]
        try:
            days = int(days_val)
        except ValueError:
            context.status_code = 400
            return get_mock_error_response(400, "Days parameter must be an integer")

        if days < 1 or days > 16:
            context.status_code = 400
            return get_mock_error_response(400, "Days parameter must be between 1 and 16")

        units = query.get("units", ["metric"])[0]
        if units not in ("metric", "imperial"):
            context.status_code = 400
            return get_mock_error_response(400, f"Unsupported units parameter: {units}")

        lang = query.get("lang", ["en"])[0]
        if lang not in ("en", "sw"):
            context.status_code = 400
            return get_mock_error_response(400, f"Unsupported language parameter: {lang}")

        ai_str = query.get("ai", ["true"])[0].lower()
        if ai_str not in ("true", "false"):
            context.status_code = 400
            return get_mock_error_response(400, "AI parameter must be true or false")

        ai = ai_str == "true"
        context.status_code = 200
        context.headers["X-RateLimit-Limit"] = "50000"
        context.headers["X-RateLimit-Remaining"] = "49850"
        context.headers["X-RateLimit-Reset"] = "1717977600"
        return get_mock_weather_response(lat=lat, lon=lon, days=days, units=units, ai=ai, lang=lang)

    # Register weather endpoint matchers
    requests_mock.get(re.compile(f"{re.escape(base)}/v1/weather.*"), json=weather_callback)
    requests_mock.get(re.compile(f"{re.escape(base)}/v1/current.*"), json=weather_callback)
    requests_mock.get(re.compile(f"{re.escape(base)}/v1/forecast.*"), json=weather_callback)
    requests_mock.get(re.compile(f"{re.escape(base)}/v1/daily.*"), json=weather_callback)
    requests_mock.get(re.compile(f"{re.escape(base)}/v1/hourly.*"), json=weather_callback)

    # GET /v1/usage
    def usage_callback(request, context):
        context.headers["Content-Type"] = "application/json"
        auth_header = request.headers.get("Authorization", "")
        if not auth_header or not auth_header.startswith("Bearer wai_") or "invalid" in auth_header:
            context.status_code = 401
            return get_mock_error_response(401, "Invalid or missing API key")
        context.status_code = 200
        return get_mock_usage_response()

    requests_mock.get(f"{base}/v1/usage", json=usage_callback)

    # GET /v1/ip-lookup
    def ip_lookup_callback(request, context):
        context.headers["Content-Type"] = "application/json"
        query = request.qs
        ip_val = query.get("ip", ["41.90.64.1"])[0]
        context.status_code = 200
        return get_mock_ip_lookup_response(ip=ip_val)

    requests_mock.get(re.compile(f"{re.escape(base)}/v1/ip-lookup.*"), json=ip_lookup_callback)
    requests_mock.get(re.compile(f"{re.escape(base)}/v1/weather-geo.*"), json=weather_callback)

    # GET /v1/webhooks
    def webhooks_callback(request, context):
        context.headers["Content-Type"] = "application/json"
        context.status_code = 200
        return get_mock_webhooks_response()

    requests_mock.get(re.compile(f"{re.escape(base)}/v1/webhooks.*"), json=webhooks_callback)

    yield requests_mock


def pytest_html_report_title(report):
    """Customize pytest HTML report title."""
    report.title = "WeatherAI API Automation Test Report"
