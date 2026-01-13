import json

import pytest

from aa_pytools.decorators.safe_execute import safe_execute


class TestSafeExecuteBasic:
    def test_successful_execution_returns_payload(self):
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
        @safe_execute
        def add_no_return(a, b):
            a + b

        result = add_no_return(2, 2)

        assert result["status"]
        assert result["result"] == "No result data"

    def test_function_name_in_success_message(self):
        @safe_execute
        def my_function():
            return "done"

        result = my_function()

        assert "my_function" in result["message"]

    def test_exception_handling_basic(self):
        @safe_execute
        def divide_by_zero():
            return 1 / 0

        result = divide_by_zero()

        assert result["status"] is False
        assert "error" in result
        assert result["error"]["type"] == "ZeroDivisionError"
        assert "time_spent" in result

    def test_preserves_function_metadata(self):
        def documented_function():
            """This is a docstring."""
            return True

        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This is a docstring."


class TestSafeExecuteWithParameters:
    def test_return_json_true(self):
        @safe_execute(return_json=True)
        def get_data():
            return {"key": "value"}

        result = get_data()

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["status"]
        assert parsed["result"] == {"key": "value"}

    def test_return_json_false_explicit(self):
        @safe_execute(return_json=False)
        def get_data():
            return "test"

        result = get_data()

        assert isinstance(result, dict)

    def test_include_trace_on_error(self):
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
        @safe_execute(include_trace=False)
        def raise_error():
            raise ValueError("Test error")

        result = raise_error()

        assert result["status"] is False
        assert "file" not in result["error"]
        assert "line" not in result["error"]

    def test_combined_parameters(self):
        @safe_execute(return_json=True, include_trace=True)
        def failing_function():
            raise RuntimeError("Combined test")

        result = failing_function()

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["status"] is False
        assert "file" in parsed["error"]
        assert parsed["error"]["type"] == "RuntimeError"


# Pytests fixtures for reusable test data
@pytest.fixture
def sample_data():
    return {"numbers": [1, 2, 3], "text": "test"}


@pytest.fixture
def decorated_function():
    @safe_execute
    def test_func(value):
        return value * 2

    return test_func


def test_with_fixture(decorated_function):
    result = decorated_function(5)
    assert result["status"]
    assert result["result"] == 10
