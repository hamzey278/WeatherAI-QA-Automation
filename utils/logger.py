import logging
import re
import sys


class SecretSanitizingFormatter(logging.Formatter):
    """Custom logging formatter that automatically redacts API keys and sensitive tokens."""

    SECRET_PATTERN = re.compile(r"(Bearer\s+wai_[A-Za-z0-9_\-]+|wai_[A-Za-z0-9_\-]+)", re.IGNORECASE)

    def format(self, record: logging.LogRecord) -> str:
        original = super().format(record)
        return self.SECRET_PATTERN.sub(r"wai_***REDACTED***", original)


def get_logger(name: str = "WeatherAI_Test") -> logging.Logger:
    """Creates a configured, secret-sanitized logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        formatter = SecretSanitizingFormatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger


logger = get_logger()
