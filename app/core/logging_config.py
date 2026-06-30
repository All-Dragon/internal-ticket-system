import os
from logging.config import dictConfig
from pathlib import Path


def _is_file_logging_enabled() -> bool:
    return os.getenv("LOG_TO_FILE", "true").lower() not in {"0", "false", "no"}


def _build_handlers() -> dict:
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "formatter": "default",
        },
    }

    if _is_file_logging_enabled():
        log_dir = Path(os.getenv("LOG_DIR", "logs"))
        log_dir.mkdir(parents=True, exist_ok=True)

        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "formatter": "default",
            "filename": str(log_dir / os.getenv("LOG_FILE", "app.log")),
            "maxBytes": int(os.getenv("LOG_MAX_BYTES", "1048576")),
            "backupCount": int(os.getenv("LOG_BACKUP_COUNT", "5")),
            "encoding": "utf-8",
        }

    return handlers


def _get_handler_names() -> list[str]:
    handlers = ["console"]

    if _is_file_logging_enabled():
        handlers.append("file")

    return handlers


def setup_logging() -> None:
    handler_names = _get_handler_names()

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": _build_handlers(),
            "loggers": {
                "app": {
                    "handlers": [],
                    "level": os.getenv("APP_LOG_LEVEL", "INFO"),
                    "propagate": True,
                },
                "uvicorn": {
                    "handlers": handler_names,
                    "level": os.getenv("UVICORN_LOG_LEVEL", "INFO"),
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": handler_names,
                    "level": os.getenv("UVICORN_ACCESS_LOG_LEVEL", "INFO"),
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": handler_names,
                    "level": os.getenv("UVICORN_LOG_LEVEL", "INFO"),
                    "propagate": False,
                },
                "sqlalchemy.engine": {
                    "handlers": handler_names,
                    "level": os.getenv("SQLALCHEMY_LOG_LEVEL", "WARNING"),
                    "propagate": False,
                },
                "": {
                    "handlers": handler_names,
                    "level": os.getenv("ROOT_LOG_LEVEL", "WARNING"),
                    "propagate": False,
                },
            },
        }
    )
