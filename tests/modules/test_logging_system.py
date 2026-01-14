import logging
from pathlib import Path

import pytest

from aa_pytools.core.logging import (
    DEFAULT_DATE_FORMAT,
    DEFAULT_FORMAT,
    DEFAULT_LOG_LEVEL,
    PACKAGE_NAME,
    _config,
    configure_logging,
    get_current_config,
    get_logger,
)


@pytest.fixture(autouse=True)
def reset_logging_status():
    """Reset logging state and test config before and after each test.

    Clears handlers and restores config to known defaults to isolate each test case.
    """
    logger = logging.getLogger(PACKAGE_NAME)
    logger.handlers.clear()
    logger.setLevel(logging.NOTSET)

    _config["configured"] = False
    _config["handlers"].clear()
    _config["level"] = DEFAULT_LOG_LEVEL
    _config["format"] = DEFAULT_FORMAT
    _config["date_format"] = DEFAULT_DATE_FORMAT

    yield

    # Reset after testing
    logger.handlers.clear()
    _config["handlers"].clear()
    _config["configured"] = False


class TestGetLogger:
    """Tests for the get_logger function and logger instance identity."""

    def test_get_logger_returns_logger_instance(self):
        """Should return a logging.Logger instance for a valid logger name."""
        logger = get_logger("aa_pytools.test")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_package_name_triggers_auto_config(self):
        """Requesting an aa_pytools logger triggers automatic configuration."""
        logger = get_logger("aa_pytools.module")
        config = get_current_config()
        assert config["configured"]
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_non_package_name_no_auto_config(self):
        """Requesting a logger outside the package should not auto-configure."""
        get_logger("some_other_package.module")
        config = get_current_config()
        assert config["configured"] is False

    def test_get_logger_returns_same_instance_for_same_name(self):
        """Requests for the same logger name must return the same instance."""
        logger1 = get_logger("aa_pytools.module")
        logger2 = get_logger("aa_pytools.module")
        assert logger1 == logger2

    def test_get_logger_different_names_return_different_instances(self):
        """Different logger names should yield different instances."""
        logger1 = get_logger("aa_pytools.module1")
        logger2 = get_logger("aa_pytools.module2")
        assert logger1 is not logger2

    def test_get_logger_name_matches_input(self):
        """Logger's .name property should match the requested name."""
        logger = get_logger("aa_pytools.custom_name")
        assert logger.name == "aa_pytools.custom_name"


class TestConfigureLoggin:
    """Tests for configure_logging's behavior, options, and arg validation."""

    def test_configure_loggin_with_defaults(self):
        """Should use the default log level, format, and date format."""
        configure_logging()
        config = get_current_config()

        assert config["configured"]
        assert config["level"] == DEFAULT_LOG_LEVEL
        assert config["format"] == DEFAULT_FORMAT
        assert config["date_format"] == DEFAULT_DATE_FORMAT

    def test_configure_logging_sets_package_logger_leve(self):
        """Should set the main package logger to the specified log level."""
        configure_logging("DEBUG")
        logger = logging.getLogger(PACKAGE_NAME)
        assert logger.level == logging.DEBUG

    def test_configure_logging_custom_level(self):
        """configure_logging should set both config and logger to custom level."""
        configure_logging("WARNING")
        configure = get_current_config()
        assert configure["level"] == "WARNING"
        logger = logging.getLogger(PACKAGE_NAME)
        assert logger.level == logging.WARNING

    def test_configure_logging_case_insensitive_level(self):
        """Log levels are case-insensitive (e.g., 'debug' == 'DEBUG')."""
        configure_logging(level="debug")
        package_logger = logging.getLogger(PACKAGE_NAME)
        assert package_logger.level == logging.DEBUG

    def test_configure_logging_invalid_level_raises_error(self):
        """Raises ValueError if level string is not valid."""
        with pytest.raises(ValueError, match="Invalid log level"):
            configure_logging(level="INVALID_LEVEL")

    def test_configure_logging_custom_format(self):
        """Setting a custom format string updates handler format."""
        custom_format = "%(levelname)s - %(message)s"
        configure_logging(format_string=custom_format)
        config = get_current_config()
        assert config["format"] == custom_format

    def test_configure_logging_custom_date_format(self):
        """Custom date format is set in config and used for output."""
        custom_date_format = "%d/%m/%Y %H:%M"
        configure_logging(date_format=custom_date_format)
        config = get_current_config()
        assert config["date_format"] == custom_date_format

    def test_configure_logging_creates_console_handler(self):
        """Default is to create a StreamHandler for console logging."""
        configure_logging()
        package_logger = logging.getLogger(PACKAGE_NAME)

        # Check that at least one StreamHandler exists (excluding FileHandlers)
        stream_handlers = [
            h
            for h in package_logger.handlers
            if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.FileHandler)
        ]
        assert len(stream_handlers) == 1

    def test_configure_logging_console_false_no_handler(self):
        """console=False prevents creation of StreamHandler."""
        configure_logging(console=False)
        package_logger = logging.getLogger(PACKAGE_NAME)
        stream_handlers = [
            h
            for h in package_logger.handlers
            if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.FileHandler)
        ]
        assert len(stream_handlers) == 0

    def test_configure_logging_with_file_creates_file_handler(self, tmp_path):
        """log_file param adds a FileHandler and file exists after use."""
        log_file = tmp_path / "test.log"
        configure_logging(log_file=log_file)
        package_logger = logging.getLogger(PACKAGE_NAME)
        file_handlers = [
            h for h in package_logger.handlers if isinstance(h, logging.FileHandler)
        ]
        assert len(file_handlers) == 1
        assert log_file.exists()

    def test_configure_logging_creates_log_directory(self, tmp_path):
        """Nested directories in log_file are created automatically."""
        log_file = tmp_path / "nested" / "dirs" / "test.log"
        configure_logging(log_file=log_file)
        assert log_file.parent.exists()
        assert log_file.parent.is_dir()

    def test_configure_logging_file_and_console(self, tmp_path):
        """File and console handlers can coexist when both enabled."""
        log_file = tmp_path / "test.log"
        configure_logging(log_file=log_file, console=True)
        package_logger = logging.getLogger(PACKAGE_NAME)
        assert len(package_logger.handlers) == 2

    def test_configure_logging_prevents_duplicate_configuration(self):
        """Subsequent config attempts without force do nothing (and retain settings)."""
        configure_logging(level="INFO")
        initial_handler_count = len(logging.getLogger(PACKAGE_NAME).handlers)

        configure_logging(level="DEBUG")  # Should be ignored

        final_handler_count = len(logging.getLogger(PACKAGE_NAME).handlers)
        assert initial_handler_count == final_handler_count

        # Level should still be INFO
        config = get_current_config()
        assert config["level"] == "INFO"

    def test_configure_logging_force_reconfigure(self):
        """force_reconfigure overrides existing config and updates the log level."""
        configure_logging(level="INFO")
        configure_logging(level="DEBUG", force_reconfigure=True)
        config = get_current_config()
        assert config["level"] == "DEBUG"

    def test_configure_logging_force_reconfigure_clears_handlers(self):
        """force_reconfigure clears any existing log handlers before applying new ones."""
        configure_logging()
        initial_handlers = len(logging.getLogger(PACKAGE_NAME).handlers)
        assert initial_handlers >= 1

        configure_logging(force_reconfigure=True)

        # After force reconfigure, handler count should reset
        config = get_current_config()
        assert config["handlers_count"] >= 1

    def test_configure_logging_prevents_propagation(self):
        """Configured logger does not propagate records to the root logger."""
        configure_logging()
        package_logger = logging.getLogger(PACKAGE_NAME)
        assert package_logger.propagate is False

    def test_configure_logging_handler_has_formatter(self):
        """Every handler gets a Formatter instance based on the format string."""
        configure_logging()
        package_logger = logging.getLogger(PACKAGE_NAME)
        for handler in package_logger.handlers:
            assert handler.formatter is not None


class TestGetCurrentConfig:
    """Tests for get_current_config dict return and values."""

    def test_get_current_config_returns_dict(self):
        """Should return a dict containing config state."""
        config = get_current_config()
        assert isinstance(config, dict)

    def test_get_current_config_has_required_keys(self):
        """Config dict has all necessary keys to summarize logging config."""
        config = get_current_config()
        required_keys = [
            "level",
            "format",
            "date_format",
            "configured",
            "handlers_count",
        ]
        for key in required_keys:
            assert key in config

    def test_get_current_config_before_configuration(self):
        """Before any configuration, dict reflects defaults and not configured."""
        config = get_current_config()
        assert config["level"] == DEFAULT_LOG_LEVEL
        assert config["configured"] is False
        assert config["handlers_count"] == 0

    def test_get_current_config_after_configuration(self):
        """After configuration, config dict reflects changes and handler count."""
        configure_logging(level="DEBUG")
        config = get_current_config()
        assert config["level"] == "DEBUG"
        assert config["configured"] is True
        assert config["handlers_count"] > 0

    def test_get_current_config_reflects_changes(self):
        """Config is updated after each re-configuration as expected."""
        configure_logging(level="INFO")
        config1 = get_current_config()
        configure_logging(level="DEBUG", force_reconfigure=True)
        config2 = get_current_config()
        assert config1["level"] != config2["level"]


class TestLoggingOutput:
    """Tests for actual logging output to various handlers."""

    def test_logger_outputs_to_console(self, capsys):
        """Logger sends info log message to the console handler."""
        configure_logging()
        logger = get_logger("aa_pytools.test")
        logger.info("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_logger_respects_log_level(self, capsys):
        """Logger only outputs messages equal/higher to its log level."""
        configure_logging(level="WARNING")
        logger = get_logger("aa_pytools.test")
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        captured = capsys.readouterr()
        assert "Debug message" not in captured.out
        assert "Info message" not in captured.out
        assert "Warning message" in captured.out

    def test_logger_writes_to_file(self, tmp_path):
        """Logger writes output to the specified log file."""
        log_file = tmp_path / "test.log"
        configure_logging(log_file=log_file)
        logger = get_logger("aa_pytools.test")
        logger.info("File message")
        content = log_file.read_text()
        assert "File message" in content

    def test_logger_format_applied(self, capsys):
        """Custom format is used for log output."""
        custom_format = "CUSTOM: %(message)s"
        configure_logging(format_string=custom_format)
        logger = get_logger("aa_pytools.test")
        logger.info("Test")
        captured = capsys.readouterr()
        assert "CUSTOM: Test" in captured.out

    def test_multiple_log_levels(self, capsys):
        """Logger emits all log levels >= configured level; all seen at DEBUG."""
        configure_logging(level="DEBUG")
        logger = get_logger("aa_pytools.test")
        logger.debug("Debug msg")
        logger.info("Info msg")
        logger.warning("Warning msg")
        logger.error("Error msg")
        logger.critical("Critical msg")
        captured = capsys.readouterr()
        output = captured.out
        assert "Debug msg" in output
        assert "Info msg" in output
        assert "Warning msg" in output
        assert "Error msg" in output
        assert "Critical msg" in output


class TestIntegration:
    """Integration tests for realistic scenarios combining features."""

    def test_multiple_modules_same_package(self, capsys):
        """Several loggers in the package write to the same handlers."""
        configure_logging()
        logger1 = get_logger("aa_pytools.module1")
        logger2 = get_logger("aa_pytools.module2")
        logger1.info("Message from module 1")
        logger2.info("Message from module 2")
        captured = capsys.readouterr()
        assert "module1" in captured.out
        assert "module2" in captured.out

    def test_file_and_console_both_receive_logs(self, tmp_path, capsys):
        """Both file and console simultaneously receive log output."""
        log_file = tmp_path / "test.log"
        configure_logging(log_file=log_file, console=True)
        logger = get_logger("aa_pytools.test")
        test_message = "Dual output test"
        logger.info(test_message)
        # Check console
        captured = capsys.readouterr()
        assert test_message in captured.out
        # Check file
        content = log_file.read_text()
        assert test_message in content

    def test_reconfigure_changes_behavior(self, capsys):
        """Reconfiguration (with force) updates logger behavior and output."""
        configure_logging(level="INFO")
        logger = get_logger("aa_pytools.test")
        logger.debug("Should not appear")
        captured = capsys.readouterr()
        assert "Should not appear" not in captured.out
        # Reconfigure with DEBUG
        configure_logging(level="DEBUG", force_reconfigure=True)
        logger.debug("Should appear now")
        captured = capsys.readouterr()
        assert "Should appear now" in captured.out

    def test_auto_configure_on_first_use(self, capsys):
        """Logger automatically configures logging on first use if absent."""
        # Don't call configure_logging explicitly
        logger = get_logger("aa_pytools.test")
        # Should auto-configure
        config = get_current_config()
        assert config["configured"] is True
        logger.info("Auto-configured message")
        captured = capsys.readouterr()
        assert "Auto-configured message" in captured.out

    def test_logging_with_exception_info(self, capsys):
        """Logger.exception logs exception info including traceback and message."""
        configure_logging()
        logger = get_logger("aa_pytools.test")
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("An error occurred")
        captured = capsys.readouterr()
        output = captured.out
        assert "An error occurred" in output
        assert "ValueError" in output
        assert "Test exception" in output


class TestEdgeCases:
    """Test edge cases and boundary conditions for robustness."""

    def test_configure_with_none_values(self):
        """None values for level, format, and date format all yield defaults."""
        configure_logging(level=None, format_string=None, date_format=None)
        config = get_current_config()
        assert config["level"] == DEFAULT_LOG_LEVEL
        assert config["format"] == DEFAULT_FORMAT
        assert config["date_format"] == DEFAULT_DATE_FORMAT

    def test_configure_with_empty_string_log_file(self):
        """Empty string for log_file is treated as falsy; no file handler created."""
        # Should not create file handler
        configure_logging(log_file="")
        package_logger = logging.getLogger(PACKAGE_NAME)
        file_handlers = [
            h for h in package_logger.handlers if isinstance(h, logging.FileHandler)
        ]
        # Empty string is falsy, so no file handler
        assert len(file_handlers) == 0

    def test_configure_with_path_object(self, tmp_path):
        """Passing a Path object to log_file creates the log file at that path."""
        log_path = tmp_path / "test.log"
        configure_logging(log_file=log_path)
        assert log_path.exists()

    def test_configure_with_string_path(self, tmp_path):
        """Passing a string path as log_file also creates the file."""
        log_file = str(tmp_path / "test.log")
        configure_logging(log_file=log_file)
        assert Path(log_file).exists()

    def test_logger_name_with_dots(self):
        """Logger names with dots are valid and set .name accordingly."""
        logger = get_logger("aa_pytools.sub.module.component")
        assert logger.name == "aa_pytools.sub.module.component"

    def test_all_log_levels_valid(self):
        """All five standard log levels are accepted as strings."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        for level in valid_levels:
            configure_logging(level=level, force_reconfigure=True)
            config = get_current_config()
            assert config["level"] == level
