"""Centralized test data repository for WeatherAI API Automation Tests."""

# Valid Location Coordinates
VALID_COORDINATES = [
    {"name": "Nairobi, Kenya", "lat": -1.2921, "lon": 36.8219},
    {"name": "Tokyo, Japan", "lat": 35.6762, "lon": 139.6503},
    {"name": "London, UK", "lat": 51.5074, "lon": -0.1278},
    {"name": "New York, USA", "lat": 40.7128, "lon": -74.0060},
    {"name": "Sydney, Australia", "lat": -33.8688, "lon": 151.2093},
]

# Coordinate Boundary & Edge Cases
LATITUDE_BOUNDARIES = [
    {"lat": -90.0, "lon": 0.0, "description": "South Pole boundary"},
    {"lat": 90.0, "lon": 0.0, "description": "North Pole boundary"},
    {"lat": 0.0, "lon": 0.0, "description": "Equator / Prime Meridian origin"},
]

INVALID_LATITUDES = [
    {"lat": -90.0001, "expected_status": 400, "reason": "Below minimum (-90)"},
    {"lat": 90.0001, "expected_status": 400, "reason": "Above maximum (90)"},
    {"lat": -500.0, "expected_status": 400, "reason": "Far below minimum"},
    {"lat": 500.0, "expected_status": 400, "reason": "Far above maximum"},
    {"lat": "invalid_string", "expected_status": 400, "reason": "Non-numeric string"},
    {"lat": "", "expected_status": 400, "reason": "Empty string"},
]

INVALID_LONGITUDES = [
    {"lon": -180.0001, "expected_status": 400, "reason": "Below minimum (-180)"},
    {"lon": 180.0001, "expected_status": 400, "reason": "Above maximum (180)"},
    {"lon": -999.0, "expected_status": 400, "reason": "Far below minimum"},
    {"lon": 999.0, "expected_status": 400, "reason": "Far above maximum"},
    {"lon": "non_numeric", "expected_status": 400, "reason": "Non-numeric string"},
    {"lon": "", "expected_status": 400, "reason": "Empty string"},
]

# Forecast Days Boundaries & Edge Cases
DAYS_TEST_CASES = [
    {"days": 1, "valid": True, "description": "Minimum valid forecast day"},
    {"days": 7, "valid": True, "description": "Standard Free plan forecast day count"},
    {"days": 14, "valid": True, "description": "Pro plan 14-day limit"},
    {"days": 0, "valid": False, "expected_status": 400, "description": "Zero days requested"},
    {"days": -1, "valid": False, "expected_status": 400, "description": "Negative days requested"},
    {"days": 30, "valid": False, "expected_status": 400, "description": "Exceeds maximum allowed limit"},
    {"days": "five", "valid": False, "expected_status": 400, "description": "Non-integer string"},
]

# Units Parameters
UNITS_TEST_CASES = [
    {"units": "metric", "valid": True},
    {"units": "imperial", "valid": True},
    {"units": "kelvin", "valid": False, "expected_status": 400},
    {"units": "invalid_unit", "valid": False, "expected_status": 400},
]

# AI Parameters
AI_TEST_CASES = [
    {"ai": "true", "valid": True},
    {"ai": "false", "valid": True},
    {"ai": "invalid_boolean", "valid": False, "expected_status": 400},
]

# Language Parameters
LANGUAGE_TEST_CASES = [
    {"lang": "en", "valid": True},
    {"lang": "sw", "valid": True},
    {"lang": "fr", "valid": False, "expected_status": 400},
    {"lang": "123", "valid": False, "expected_status": 400},
]

# Authentication Scenarios
AUTH_SCENARIOS = [
    {"name": "Valid API Key", "key": "wai_valid_sample_key_12345", "expected_status": 200},
    {"name": "Missing Authorization Header", "headers": {}, "expected_status": 401},
    {"name": "Invalid API Key", "key": "wai_invalid_token_9999", "expected_status": 401},
    {"name": "Malformed Authorization Header", "raw_header": "Basic wai_invalid_token", "expected_status": 401},
    {"name": "Empty Bearer Token", "raw_header": "Bearer ", "expected_status": 401},
]
