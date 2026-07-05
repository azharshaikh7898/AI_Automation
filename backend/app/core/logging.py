import logging
import logging.config
from collections.abc import Mapping

from app.core.config import settings


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def build_logging_config() -> Mapping[str, object]:
    """
    Return a dictConfig-compatible logging configuration.

    The configuration keeps output simple and production-appropriate while
    remaining easy to extend with JSON formatters or external log handlers later.
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": settings.log_level,
            }
        },
        "loggers": {
            "app": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": "INFO" if settings.debug else "WARNING",
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": settings.log_level,
        },
    }


def configure_logging() -> None:
    """
    Apply the application's centralized logging configuration.
    """
    logging.config.dictConfig(build_logging_config())


def get_logger(name: str) -> logging.Logger:
    """
    Return a namespaced logger for app modules.
    """
    return logging.getLogger(name)
