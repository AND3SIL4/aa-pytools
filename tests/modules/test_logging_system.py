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
    def test_get_logger_returns_logger_instance(self):
        logger = get_logger("aa_pytools.test")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_package_name_triggers_auto_config(self):
        logger = get_logger("aa_pytools.module")
        config = get_current_config()
        assert config["configured"]
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_non_package_name_no_auto_config(self):
        get_logger("some_other_package.module")
        config = get_current_config()
        assert config["configured"] is False

    def test_get_logger_returns_same_instance_for_same_name(self):
        logger1 = get_logger("aa_pytools.module")
        logger2 = get_logger("aa_pytools.module")
        assert logger1 == logger2

    def test_get_logger_different_names_return_different_instances(self):
        logger1 = get_logger("aa_pytools.module1")
        logger2 = get_logger("aa_pytools.module2")
        assert logger1 is not logger2

    def test_get_logger_name_matches_input(self):
        logger = get_logger("aa_pytools.custom_name")
        assert logger.name == "aa_pytools.custom_name"


class TestConfigureLoggin:
    def test_configure_loggin_with_defaults(self):
        configure_logging()
        config = get_current_config()

        assert config["configured"]
        assert config["level"] == DEFAULT_LOG_LEVEL
        assert config["format"] == DEFAULT_FORMAT
        assert config["date_format"] == DEFAULT_DATE_FORMAT

    def test_configure_logging_sets_package_logger_leve(self):
        configure_logging("DEBUG")
        logger = logging.getLogger(PACKAGE_NAME)
        assert logger.level == logging.DEBUG

    def test_configure_logging_custom_level(self):
        configure_logging("WARNING")
        configure = get_current_config()
        assert configure["level"] == "WARNING"
        logger = logging.getLogger(PACKAGE_NAME)
        assert logger.level == logging.WARNING

    def test_configure_logging_case_insensitive_level(self):
        """Test that log level is case-insensitive."""
        configure_logging(level="debug")

        package_logger = logging.getLogger(PACKAGE_NAME)
        assert package_logger.level == logging.DEBUG

    def test_configure_logging_invalid_level_raises_error(self):
        """Test that invalid log level raises ValueError."""
        with pytest.raises(ValueError, match="Invalid log level"):
            configure_logging(level="INVALID_LEVEL")

    def test_configure_logging_custom_format(self):
        """Test configuration with custom format string."""
        custom_format = "%(levelname)s - %(message)s"
        configure_logging(format_string=custom_format)

        config = get_current_config()
        assert config["format"] == custom_format

    def test_configure_logging_custom_date_format(self):
        """Test configuration with custom date format."""
        custom_date_format = "%d/%m/%Y %H:%M"
        configure_logging(date_format=custom_date_format)

        config = get_current_config()
        assert config["date_format"] == custom_date_format

    def test_configure_logging_creates_console_handler(self):
        """Test that configure_logging creates console handler by default."""
        configure_logging()

        package_logger = logging.getLogger(PACKAGE_NAME)

        # Check that at least one StreamHandler exists
        stream_handlers = [
            h
            for h in package_logger.handlers
            if isinstance(h, logging.StreamHandler)
            and not isinstance(h, logging.FileHandler)
        ]
        assert len(stream_handlers) == 1

    def test_configure_logging_console_false_no_handler(self):
        """Test that console=False doesn't create console handler."""
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
        """Test that log_file parameter creates file handler."""
        log_file = tmp_path / "test.log"
        configure_logging(log_file=log_file)

        package_logger = logging.getLogger(PACKAGE_NAME)

        file_handlers = [
            h for h in package_logger.handlers if isinstance(h, logging.FileHandler)
        ]
        assert len(file_handlers) == 1
        assert log_file.exists()

    def test_configure_logging_creates_log_directory(self, tmp_path):
        """Test that configure_logging creates nested directories."""
        log_file = tmp_path / "nested" / "dirs" / "test.log"
        configure_logging(log_file=log_file)

        assert log_file.parent.exists()
        assert log_file.parent.is_dir()

    def test_configure_logging_file_and_console(self, tmp_path):
        """Test that both file and console handlers can coexist."""
        log_file = tmp_path / "test.log"
        configure_logging(log_file=log_file, console=True)

        package_logger = logging.getLogger(PACKAGE_NAME)

        assert len(package_logger.handlers) == 2

    def test_configure_logging_prevents_duplicate_configuration(self):
        """Test that configure_logging doesn't configure twice."""
        configure_logging(level="INFO")
        initial_handler_count = len(logging.getLogger(PACKAGE_NAME).handlers)

        configure_logging(level="DEBUG")  # Should be ignored

        final_handler_count = len(logging.getLogger(PACKAGE_NAME).handlers)
        assert initial_handler_count == final_handler_count

        # Level should still be INFO
        config = get_current_config()
        assert config["level"] == "INFO"

    def test_configure_logging_force_reconfigure(self):
        """Test that force_reconfigure=True allows reconfiguration."""
        configure_logging(level="INFO")

        configure_logging(level="DEBUG", force_reconfigure=True)

        config = get_current_config()
        assert config["level"] == "DEBUG"

    def test_configure_logging_force_reconfigure_clears_handlers(self):
        """Test that force_reconfigure clears existing handlers."""
        configure_logging()
        initial_handlers = len(logging.getLogger(PACKAGE_NAME).handlers)
        assert initial_handlers >= 1

        configure_logging(force_reconfigure=True)

        # After force reconfigure, handler count should reset
        config = get_current_config()
        assert config["handlers_count"] >= 1

    def test_configure_logging_prevents_propagation(self):
        """Test that package logger doesn't propagate to root."""
        configure_logging()

        package_logger = logging.getLogger(PACKAGE_NAME)
        assert package_logger.propagate is False

    def test_configure_logging_handler_has_formatter(self):
        """Test that handlers have proper formatter applied."""
        configure_logging()

        package_logger = logging.getLogger(PACKAGE_NAME)

        for handler in package_logger.handlers:
            assert handler.formatter is not None


class TestGetCurrentConfig:
    def test_get_current_config_returns_dict(self):
        """Test that get_current_config returns a dictionary."""
        config = get_current_config()
        assert isinstance(config, dict)

    def test_get_current_config_has_required_keys(self):
        """Test that config dict has all required keys."""
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
        """Test config state before any configuration."""
        config = get_current_config()

        assert config["level"] == DEFAULT_LOG_LEVEL
        assert config["configured"] is False
        assert config["handlers_count"] == 0

    def test_get_current_config_after_configuration(self):
        """Test config state after configuration."""
        configure_logging(level="DEBUG")
        config = get_current_config()

        assert config["level"] == "DEBUG"
        assert config["configured"] is True
        assert config["handlers_count"] > 0

    def test_get_current_config_reflects_changes(self):
        """Test that config reflects configuration changes."""
        configure_logging(level="INFO")
        config1 = get_current_config()

        configure_logging(level="DEBUG", force_reconfigure=True)
        config2 = get_current_config()

        assert config1["level"] != config2["level"]


class TestLoggingOutput:
    def test_logger_outputs_to_console(self, capsys):
        """Test that logger writes to console."""
        configure_logging()
        logger = get_logger("aa_pytools.test")

        logger.info("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_logger_respects_log_level(self, capsys):
        """Test that logger respects configured log level."""
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
        """Test that logger writes to file."""
        log_file = tmp_path / "test.log"
        configure_logging(log_file=log_file)
        logger = get_logger("aa_pytools.test")

        logger.info("File message")

        content = log_file.read_text()
        assert "File message" in content

    def test_logger_format_applied(self, capsys):
        """Test that custom format is applied to output."""
        custom_format = "CUSTOM: %(message)s"
        configure_logging(format_string=custom_format)
        logger = get_logger("aa_pytools.test")

        logger.info("Test")

        captured = capsys.readouterr()
        assert "CUSTOM: Test" in captured.out

    def test_multiple_log_levels(self, capsys):
        """Test different log levels produce correct output."""
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
    """Integration tests for realistic scenarios."""

    def test_multiple_modules_same_package(self, capsys):
        """Test logging from multiple modules in the package."""
        configure_logging()

        logger1 = get_logger("aa_pytools.module1")
        logger2 = get_logger("aa_pytools.module2")

        logger1.info("Message from module 1")
        logger2.info("Message from module 2")

        captured = capsys.readouterr()
        assert "module1" in captured.out
        assert "module2" in captured.out

    def test_file_and_console_both_receive_logs(self, tmp_path, capsys):
        """Test that logs go to both file and console."""
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
        """Test that reconfiguration changes logging behavior."""
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
        """Test that logger auto-configures on first use."""
        # Don't call configure_logging explicitly
        logger = get_logger("aa_pytools.test")

        # Should auto-configure
        config = get_current_config()
        assert config["configured"] is True

        logger.info("Auto-configured message")

        captured = capsys.readouterr()
        assert "Auto-configured message" in captured.out

    def test_logging_with_exception_info(self, capsys):
        """Test logging with exception information."""
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
    """Test edge cases and boundary conditions."""

    def test_configure_with_none_values(self):
        """Test that None values use defaults."""
        configure_logging(level=None, format_string=None, date_format=None)

        config = get_current_config()
        assert config["level"] == DEFAULT_LOG_LEVEL
        assert config["format"] == DEFAULT_FORMAT
        assert config["date_format"] == DEFAULT_DATE_FORMAT

    def test_configure_with_empty_string_log_file(self):
        """Test behavior with empty string for log_file."""
        # Should not create file handler
        configure_logging(log_file="")

        package_logger = logging.getLogger(PACKAGE_NAME)
        file_handlers = [
            h for h in package_logger.handlers if isinstance(h, logging.FileHandler)
        ]

        # Empty string is falsy, so no file handler
        assert len(file_handlers) == 0

    def test_configure_with_path_object(self, tmp_path):
        """Test that Path objects work for log_file."""
        log_path = tmp_path / "test.log"
        configure_logging(log_file=log_path)

        assert log_path.exists()

    def test_configure_with_string_path(self, tmp_path):
        """Test that string paths work for log_file."""
        log_file = str(tmp_path / "test.log")
        configure_logging(log_file=log_file)

        assert Path(log_file).exists()

    def test_logger_name_with_dots(self):
        """Test that logger names with dots work correctly."""
        logger = get_logger("aa_pytools.sub.module.component")
        assert logger.name == "aa_pytools.sub.module.component"

    def test_all_log_levels_valid(self):
        """Test that all standard log levels are accepted."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in valid_levels:
            configure_logging(level=level, force_reconfigure=True)
            config = get_current_config()
            assert config["level"] == level
