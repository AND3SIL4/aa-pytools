import logging
import sys
from pathlib import Path
from typing import Literal

# Type alias for log levels
LOG_LEVEL = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
# Default configuration
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# Package logger name
PACKAGE_NAME = "aa_pytools"

# Set the global configuration state
_config = dict[str, any] = {
    "level": DEFAULT_LOG_LEVEL,
    "format": DEFAULT_FORMAT,
    "date_format": DEFAULT_DATE_FORMAT,
    "handlers": [],
    "configured": False,
}


def get_logger(name: str) -> logging.Logger:
    # Get or create a logging instance
    logger = logging.getLogger(name)
    if name.startswith(PACKAGE_NAME) and not _config["configured"]:
        configure_logging()  # Set the default configuration

    return logger


def configure_logging(
    level: LOG_LEVEL | None = None,
    format_string: str | None = None,
    date_format: str | None = None,
    log_file: Path | str | None = None,
    console: bool = True,
    force_reconfigure: bool = False,
) -> None:
    if _config["configured"] and not force_reconfigure:
        return

    # Update configuration
    _config["level"] = level or DEFAULT_LOG_LEVEL
    _config["format"] = format_string or DEFAULT_FORMAT
    _config["date_format"] = date_format or DEFAULT_DATE_FORMAT

    # Get the root logger for the package
    package_logger = logging.getLogger(PACKAGE_NAME)
    try:
        package_logger.setLevel(getattr(logging, _config["level"].upper()))
    except AttributeError:
        raise ValueError(f"Invalid log level: {_config['level']}")

    # Clear existing handlers if reconfiguring
    if force_reconfigure:
        package_logger.handlers.clear()
        _config["handlers"].clear()
        _config["configured"] = False

    # Create formatter
    formatter = logging.Formatter(fmt=_config["format"], datefmt=_config["date_format"])

    # Add console handler
    if console and not any(
        isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        for h in package_logger.handlers
    ):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        package_logger.addHandler(console_handler)
        _config["handlers"].append(console_handler)

    # Add file handler if requested
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        if not any(isinstance(h, logging.FileHandler) for h in package_logger.handlers):
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)
            package_logger.addHandler(file_handler)
            _config["handlers"].append(file_handler)

    # Prevent propagation to root logger
    package_logger.propagate = False
    _config["configured"] = True


def get_current_config() -> dict[str, any]:
    return {
        "level": _config["level"],
        "format": _config["format"],
        "date_format": _config["date_format"],
        "configured": _config["configured"],
        "handlers_count": len(_config["handlers"]),
    }

