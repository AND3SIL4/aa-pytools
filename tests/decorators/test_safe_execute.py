import json

import pytest

from aa_pytools.decorators.safe_execute import safe_execute


class TestSafeExecuteBasic:
    def test_successful_execution_returns_payload(self):
        """
        Test that a basic function wrapped with @safe_execute returns
        a dictionary payload indicating successful execution, containing
        'status', 'result', 'message', and 'time_spent' fields.
        """

        @safe_execute
        def add(a, b):
            return a + b

        result = add(2, 2)

        assert isinstance(result, dict)
        assert result["status"]
        assert result["result"] == 4
        assert "message" in result
        assert "time_spent" in result
        assert isinstance(result["time_spent"], (int, float))

    def test_function_with_no_return_value(self):
        """
        Test that if the decorated function does not return anything,
        the payload's 'result' is set to the default no-result string.
        """

        @safe_execute
        def add_no_return(a, b):
            a + b

        result = add_no_return(2, 2)

        assert result["status"]
        assert result["result"] == "No result data"

    def test_function_name_in_success_message(self):
        """
        Test that the success message in the payload includes the name of
        the function that was successfully executed.
        """

        @safe_execute
        def my_function():
            return "done"

        result = my_function()

        assert "my_function" in result["message"]

    def test_exception_handling_basic(self):
        """
        Test that when the decorated function raises an exception,
        the payload indicates failure, provides an 'error' field with the
        exception type, and includes timing information.
        """

        @safe_execute
        def divide_by_zero():
            return 1 / 0

        result = divide_by_zero()

        assert result["status"] is False
        assert "error" in result
        assert result["error"]["type"] == "ZeroDivisionError"
        assert "time_spent" in result

    def test_preserves_function_metadata(self):
        """
        Test that the decorator does not alter the __name__ or __doc__ properties
        of the original function when not applied.
        """

        def documented_function():
            """This is a docstring."""
            return True

        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This is a docstring."


class TestSafeExecuteWithParameters:
    def test_return_json_true(self):
        """
        Test that when @safe_execute(return_json=True) is used, the wrapper returns
        a JSON string payload and not a dictionary.
        """

        @safe_execute(return_json=True)
        def get_data():
            return {"key": "value"}

        result = get_data()

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["status"]
        assert parsed["result"] == {"key": "value"}

    def test_return_json_false_explicit(self):
        """
        Test that when @safe_execute(return_json=False) is used, the wrapper returns
        a dictionary payload (not a string).
        """

        @safe_execute(return_json=False)
        def get_data():
            return "test"

        result = get_data()

        assert isinstance(result, dict)

    def test_include_trace_on_error(self):
        """
        Test that when include_trace=True, errors include filename and line number
        in the 'error' dict when an exception is raised.
        """

        @safe_execute(include_trace=True)
        def raise_error():
            raise ValueError("Test error")

        result = raise_error()

        assert result["status"] is False
        assert "file" in result["error"]
        assert "line" in result["error"]
        assert isinstance(result["error"]["line"], int)
        assert result["error"]["file"].endswith(".py")

    def test_include_trace_false(self):
        """
        Test that when include_trace=False, 'file' and 'line' are not included in
        the error payload on exception.
        """

        @safe_execute(include_trace=False)
        def raise_error():
            raise ValueError("Test error")

        result = raise_error()

        assert result["status"] is False
        assert "file" not in result["error"]
        assert "line" not in result["error"]

    def test_combined_parameters(self):
        """
        Test that combining return_json=True and include_trace=True works as expected:
        error payload is stringified JSON and includes trace information on failure.
        """

        @safe_execute(return_json=True, include_trace=True)
        def failing_function():
            raise RuntimeError("Combined test")

        result = failing_function()

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["status"] is False
        assert "file" in parsed["error"]
        assert parsed["error"]["type"] == "RuntimeError"


# Pytest fixtures for reusable test data


@pytest.fixture
def sample_data():
    """Fixture providing sample data as a dict."""
    return {"numbers": [1, 2, 3], "text": "test"}


@pytest.fixture
def decorated_function():
    """Fixture providing a sample function wrapped with safe_execute."""

    @safe_execute
    def test_func(value):
        return value * 2

    return test_func


def test_with_fixture(decorated_function):
    """Test using the decorated_function fixture to ensure correct wrapping."""
    result = decorated_function(5)
    assert result["status"]
    assert result["result"] == 10
