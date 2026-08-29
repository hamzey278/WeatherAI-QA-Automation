from typing import Any
import requests
from config.settings import settings
from utils.logger import logger


class WeatherAPIClient:
    """Reusable API Client for WeatherAI Developer Platform REST endpoints."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: int | None = None,
    ) -> None:
        self.base_url = (base_url or settings.WEATHER_API_BASE_URL).rstrip("/")
        self.api_key = api_key if api_key is not None else settings.WEATHER_API_KEY
        self.timeout = timeout or settings.API_TIMEOUT
        self.session = requests.Session()

    def _get_headers(self, custom_headers: dict[str, str] | None = None) -> dict[str, str]:
        """Construct standard authorization and content headers."""
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        raw_header_override: str | None = None,
    ) -> requests.Response:
        """Executes an HTTP request against the WeatherAI API with logging and timing metrics."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req_headers = self._get_headers(headers)

        if raw_header_override is not None:
            if raw_header_override == "":
                req_headers.pop("Authorization", None)
            else:
                req_headers["Authorization"] = raw_header_override

        # Clean params None values
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}

        # Log request without leaking secrets
        sanitized_headers = {k: ("***REDACTED***" if k.lower() == "authorization" else v) for k, v in req_headers.items()}
        logger.info(f"API Request: {method.upper()} {url} | Params: {clean_params} | Headers: {sanitized_headers}")

        response = self.session.request(
            method=method,
            url=url,
            params=clean_params,
            json=json_data,
            files=files,
            headers=req_headers,
            timeout=self.timeout,
        )

        logger.info(f"API Response: {response.status_code} {response.reason} | Time: {response.elapsed.total_seconds() * 1000:.2f}ms")
        return response

    # Weather Endpoints
    def get_weather(
        self,
        lat: float | str | None = -1.2921,
        lon: float | str | None = 36.8219,
        days: int | str | None = None,
        units: str | None = None,
        ai: bool | str | None = None,
        lang: str | None = None,
        headers: dict[str, str] | None = None,
        raw_auth_header: str | None = None,
    ) -> requests.Response:
        """GET /v1/weather - Core weather and forecast endpoint."""
        params = {"lat": lat, "lon": lon, "days": days, "units": units, "ai": ai, "lang": lang}
        return self.request("GET", "/v1/weather", params=params, headers=headers, raw_header_override=raw_auth_header)

    def get_current(
        self,
        lat: float | str | None = -1.2921,
        lon: float | str | None = 36.8219,
        units: str | None = None,
        lang: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """GET /v1/current - Current weather conditions."""
        params = {"lat": lat, "lon": lon, "units": units, "lang": lang}
        return self.request("GET", "/v1/current", params=params, headers=headers)

    def get_forecast(
        self,
        lat: float | str | None = -1.2921,
        lon: float | str | None = 36.8219,
        days: int | str | None = None,
        units: str | None = None,
        lang: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """GET /v1/forecast - Multi-day forecast alias endpoint."""
        params = {"lat": lat, "lon": lon, "days": days, "units": units, "lang": lang}
        return self.request("GET", "/v1/forecast", params=params, headers=headers)

    def get_daily(
        self,
        lat: float | str | None = -1.2921,
        lon: float | str | None = 36.8219,
        days: int | str | None = None,
        units: str | None = None,
        lang: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """GET /v1/daily - Daily aggregated forecast."""
        params = {"lat": lat, "lon": lon, "days": days, "units": units, "lang": lang}
        return self.request("GET", "/v1/daily", params=params, headers=headers)

    def get_hourly(
        self,
        lat: float | str | None = -1.2921,
        lon: float | str | None = 36.8219,
        units: str | None = None,
        lang: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """GET /v1/hourly - Hourly weather forecast."""
        params = {"lat": lat, "lon": lon, "units": units, "lang": lang}
        return self.request("GET", "/v1/hourly", params=params, headers=headers)

    def get_weather_geo(
        self,
        lat: float | str | None = None,
        lon: float | str | None = None,
        ip: str | None = "auto",
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """GET /v1/weather-geo - Geo-targeted weather detection."""
        params = {"lat": lat, "lon": lon, "ip": ip}
        return self.request("GET", "/v1/weather-geo", params=params, headers=headers)

    def get_ip_lookup(
        self,
        ip: str | None = "auto",
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """GET /v1/ip-lookup - IP resolution endpoint."""
        params = {"ip": ip}
        return self.request("GET", "/v1/ip-lookup", params=params, headers=headers)

    # Usage & Quota
    def get_usage(self, headers: dict[str, str] | None = None, raw_auth_header: str | None = None) -> requests.Response:
        """GET /v1/usage - Usage analytics and quota monitoring."""
        return self.request("GET", "/v1/usage", headers=headers, raw_header_override=raw_auth_header)

    # Webhooks
    def create_webhook(
        self,
        url: str,
        lat: float,
        lon: float,
        triggers: list[str],
        timezone: str = "America/Los_Angeles",
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """POST /v1/webhooks - Register a new webhook subscription."""
        payload = {"url": url, "lat": lat, "lon": lon, "triggers": triggers, "timezone": timezone}
        return self.request("POST", "/v1/webhooks", json_data=payload, headers=headers)

    def get_webhooks(self, headers: dict[str, str] | None = None) -> requests.Response:
        """GET /v1/webhooks - List active webhook subscriptions."""
        return self.request("GET", "/v1/webhooks", headers=headers)

    def delete_webhook(self, webhook_id: str, headers: dict[str, str] | None = None) -> requests.Response:
        """DELETE /v1/webhooks/:id - Remove a webhook subscription."""
        return self.request("DELETE", f"/v1/webhooks/{webhook_id}", headers=headers)
