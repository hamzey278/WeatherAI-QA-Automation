from typing import Any, Sequence
import jsonschema
import requests
from utils.logger import logger


def assert_status_code(response: requests.Response, expected_status: int) -> None:
    """Assert that the HTTP response status code matches expected status code."""
    assert (
        response.status_code == expected_status
    ), f"Expected HTTP status {expected_status}, but got {response.status_code}. Body: {response.text[:300]}"


def assert_json_content_type(response: requests.Response) -> None:
    """Assert that the response Content-Type header indicates JSON format."""
    content_type = response.headers.get("Content-Type", "")
    assert (
        "application/json" in content_type.lower()
    ), f"Expected Content-Type 'application/json', got '{content_type}'"


def assert_error_response(response: requests.Response, expected_status: int) -> dict[str, Any]:
    """Assert status code, JSON format, and standard error structure."""
    assert_status_code(response, expected_status)
    assert_json_content_type(response)
    data = response.json()
    assert isinstance(data, dict), f"Expected error payload to be a JSON object, got {type(data)}"
    assert "error" in data or "message" in data or "code" in data, (
        f"Error response payload missing error descriptor keys. Keys found: {list(data.keys())}"
    )
    return data


def assert_required_fields(data: dict[str, Any], required_fields: Sequence[str]) -> None:
    """Assert that all required top-level keys exist in the response JSON dictionary."""
    missing = [field for field in required_fields if field not in data]
    assert not missing, f"Missing required fields in response: {missing}. Available fields: {list(data.keys())}"


def assert_valid_coordinates(lat: float, lon: float) -> None:
    """Assert that latitude and longitude conform to geographic bounds."""
    assert -90.0 <= lat <= 90.0, f"Latitude {lat} is out of valid bounds [-90, 90]"
    assert -180.0 <= lon <= 180.0, f"Longitude {lon} is out of valid bounds [-180, 180]"


def assert_rate_limit_headers(response: requests.Response) -> None:
    """Assert presence and validity of rate limit headers if returned by API."""
    headers = response.headers
    if "X-RateLimit-Limit" in headers:
        limit = int(headers["X-RateLimit-Limit"])
        assert limit > 0, f"X-RateLimit-Limit should be positive, got {limit}"
    if "X-RateLimit-Remaining" in headers:
        remaining = int(headers["X-RateLimit-Remaining"])
        assert remaining >= 0, f"X-RateLimit-Remaining should be non-negative, got {remaining}"
    if "X-RateLimit-Reset" in headers:
        reset_time = int(headers["X-RateLimit-Reset"])
        assert reset_time > 0, f"X-RateLimit-Reset should be valid timestamp, got {reset_time}"


def assert_response_time(elapsed_seconds: float, threshold_ms: float = 3000.0) -> None:
    """Assert that response time is within specified performance threshold."""
    elapsed_ms = elapsed_seconds * 1000.0
    logger.info(f"Response latency: {elapsed_ms:.2f}ms (Threshold: {threshold_ms:.2f}ms)")
    assert (
        elapsed_ms <= threshold_ms
    ), f"Response time of {elapsed_ms:.2f}ms exceeded threshold of {threshold_ms:.2f}ms"


def assert_schema_valid(instance: dict[str, Any], schema: dict[str, Any]) -> None:
    """Validate JSON response instance against a JSON Schema dictionary."""
    try:
        jsonschema.validate(instance=instance, schema=schema)
    except jsonschema.ValidationError as err:
        raise AssertionError(f"JSON Schema validation failed for path {list(err.path)}: {err.message}") from err
