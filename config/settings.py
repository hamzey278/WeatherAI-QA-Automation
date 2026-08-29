import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Centralized configuration manager for WeatherAI API Automation Framework."""

    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY") or "wai_demo_key"
    WEATHER_API_BASE_URL: str = os.getenv("WEATHER_API_BASE_URL", "https://api.weather-ai.co").rstrip("/")
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "10"))
    PERFORMANCE_THRESHOLD_MS: float = float(os.getenv("PERFORMANCE_THRESHOLD_MS", "3000"))
    USE_MOCK_SERVER: bool = os.getenv("USE_MOCK_SERVER", "false").lower() in ("true", "1", "yes")

    @classmethod
    def get_auth_headers(cls, override_key: str | None = None) -> dict[str, str]:
        """Generate Authorization headers using specified or configured key."""
        key = override_key if override_key is not None else cls.WEATHER_API_KEY
        headers = {"Content-Type": "application/json"}
        if key:
            headers["Authorization"] = f"Bearer {key}"
        return headers


settings = Settings()
