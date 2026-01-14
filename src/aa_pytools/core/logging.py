"""
Logging system for aa_pytools.

This module provides a convenient logging setup for use in the aa_pytools package.
It supports easy logger creation, configurable formatting, and centralized configuration
(including log level, output file, and date/detail formatting). It is designed to be
auto-configuring on first use within the package.

Exports:
    - LOG_LEVEL: Literal type for log levels.
    - DEFAULT_LOG_LEVEL, DEFAULT_FORMAT, DEFAULT_DATE_FORMAT: Default logging settings.
    - PACKAGE_NAME: Name of the root package logger.
    - configure_logging: Configure or reconfigure the package logging system.
    - get_logger: Retrieve a logger for the given name (auto-configures on first use).
    - get_current_config: Return the current logging configuration for inspection.
"""

import logging
import sys
from pathlib import Path
from typing import Literal

# Type alias for log levels
LOG_LEVEL = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Default configuration values for logging
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Package logger name -- used for internal logging
PACKAGE_NAME = "aa_pytools"

# Set the global configuration state for logging (internal)
_config: dict[str, any] = {
    "level": DEFAULT_LOG_LEVEL,
    "format": DEFAULT_FORMAT,
    "date_format": DEFAULT_DATE_FORMAT,
    "handlers": [],
    "configured": False,
}


def get_logger(name: str) -> logging.Logger:
    """
    Retrieve a logger with the specified name.

    If the logger name begins with the package name and logging has not yet been
    configured, this will auto-configure logging with default options.

    Args:
        name (str): The name of the logger to retrieve.

    Returns:
        logging.Logger: The logger for the given name.
    """
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
    """
    Configure or reconfigure package logging.

    This sets up handlers and formats for the package logger. It can add console and/or
    file logging and allows for repeated reconfiguration.

    Args:
        level (LOG_LEVEL | None): Logging verbosity. Default uses 'INFO'.
        format_string (str | None): Logging output format. Uses package default if None.
        date_format (str | None): Format for timestamps. Defaults to package-wide format.
        log_file (Path | str | None): If provided, logs are also written to this file.
        console (bool): If True, enable logging to the console (stdout).
        force_reconfigure (bool): If True, forcibly reset config and handlers.
    """
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
    """
    Return the current logging configuration state (for introspection/testing).

    Returns:
        dict: Dictionary with current log level, format, configured status,
              date format, and number of handlers.
    """
    return {
        "level": _config["level"],
        "format": _config["format"],
        "date_format": _config["date_format"],
        "configured": _config["configured"],
        "handlers_count": len(_config["handlers"]),
    }
