"""Contract-compliant mock response provider for WeatherAI API based on official documentation."""

from typing import Any


def get_mock_weather_response(
    lat: float = -1.2921,
    lon: float = 36.8219,
    days: int = 7,
    units: str = "metric",
    ai: bool = True,
    lang: str = "en",
) -> dict[str, Any]:
    """Generates standard /v1/weather response JSON."""
    temp_unit = "C" if units == "metric" else "F"
    speed_unit = "m/s" if units == "metric" else "mph"

    forecast_items = []
    for day_offset in range(days):
        forecast_items.append(
            {
                "date": f"2026-08-{29 + day_offset:02d}",
                "temp_max": 24.5 + day_offset,
                "temp_min": 15.0 + day_offset,
                "precipitation_mm": 2.5 if day_offset % 2 == 0 else 0.0,
                "condition": "Partly Cloudy" if day_offset % 2 == 0 else "Sunny",
                "humidity_pct": 65,
                "wind_speed": 4.2,
            }
        )

    response = {
        "location": {
            "lat": float(lat),
            "lon": float(lon),
            "city": "Nairobi",
            "country": "Kenya",
            "timezone": "Africa/Nairobi",
        },
        "units": {"temperature": temp_unit, "wind_speed": speed_unit},
        "current": {
            "timestamp": "2026-08-29T08:00:00Z",
            "temperature": 22.4,
            "humidity": 68,
            "wind_speed": 3.8,
            "condition": "Partly Cloudy",
            "uv_index": 6.2,
        },
        "forecast": forecast_items,
        "forecast_days": days,
        "language": lang,
    }

    if ai:
        response["ai_summary"] = (
            "Favorable weather conditions expected. Moderate rainfall on alternate days "
            "will benefit tea and maize crops in the region."
        )

    return response


def get_mock_usage_response() -> dict[str, Any]:
    """Generates standard /v1/usage response JSON."""
    return {
        "account_id": "acc_weatherai_demo_123",
        "plan": "free",
        "requests": {"used": 150, "limit": 50000, "remaining": 49850},
        "ai_requests": {"used": 25, "limit": 1000, "remaining": 975},
        "billing_period": {
            "start": "2026-08-01T00:00:00Z",
            "end": "2026-08-31T23:59:59Z",
            "resets_at": "2026-09-01T00:00:00Z",
        },
    }


def get_mock_ip_lookup_response(ip: str = "41.90.64.1") -> dict[str, Any]:
    """Generates standard /v1/ip-lookup response JSON."""
    return {
        "ip": ip,
        "ip_hash": "a3f1b2c3d4e5f6a7b8c9d0e1f2a3b4c5",
        "ip_version": "v4",
        "geo": {
            "lat": 34.0522,
            "lon": -118.2437,
            "city": "Los Angeles",
            "region": "California",
            "country": "US",
            "timezone": "America/Los_Angeles",
        },
    }


def get_mock_webhooks_response() -> dict[str, Any]:
    """Generates standard GET /v1/webhooks response JSON."""
    return {
        "webhooks": [
            {
                "id": "wh_abc12345",
                "url": "https://yourapp.com/weather-hook",
                "lat": 34.0522,
                "lon": -118.2437,
                "triggers": ["rain", "extreme_wind"],
                "timezone": "America/Los_Angeles",
                "active": True,
                "createdAt": "2026-08-01T10:00:00Z",
            }
        ]
    }


def get_mock_error_response(status_code: int = 400, message: str = "Bad Request") -> dict[str, Any]:
    """Generates standard WeatherAI error response JSON."""
    code_map = {
        400: "INVALID_PARAMETER",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_SERVER_ERROR",
        503: "SERVICE_UNAVAILABLE",
    }
    return {
        "error": {
            "code": code_map.get(status_code, "ERROR"),
            "message": message,
            "status": status_code,
        }
    }
