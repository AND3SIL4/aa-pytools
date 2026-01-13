import functools
import json
import os
import sys
import time

# --- Set up the constant values
DEFAULT_SUCCESS_MSG = "execute successfully"
DEFAULT_NO_RESULT = "No result data"


def safe_execute(
    _func: callable = None, *, return_json: bool = False, include_trace: bool = False
) -> callable:
    """
    Decorator that execute a function safely, catching exceptions and returning
    a standardized result payload.

    Can be used with or without parameters:
        @safe_execute
        @safe_execute(return_json=True, include_trace=True)
    """

    def decorator(func: callable) -> callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> dict[str, any] | str:
            start_time = time.perf_counter()

            try:
                result = func(*args, **kwargs)
                elapsed = round(time.perf_counter() - start_time, 6)

                payload = {
                    "status": True,
                    "message": f"Function {func.__name__} {DEFAULT_SUCCESS_MSG}",
                    "result": result if result is not None else DEFAULT_NO_RESULT,
                    "time_spent": elapsed,
                }

                return json.dumps(payload) if return_json else payload

            except Exception as e:
                # todo: apply the logging system, import from core in this project
                # create a new instance and apply the logging system if the argument requires
                elapsed = round(time.perf_counter() - start_time, 6)
                exc_type, _, exc_tb = sys.exc_info()

                fname = None
                line_no = None

                if include_trace and exc_tb:
                    tb = exc_tb
                    while tb:
                        if tb.tb_frame.f_code.co_name == func.__name__:
                            break
                        tb = tb.tb_next

                    frame = tb if tb else exc_tb
                    fname = os.path.basename(frame.tb_frame.f_code.co_filename)
                    line_no = frame.tb_lineno

                error_payload = {"type": exc_type.__name__, "message": str(e)}

                if include_trace:
                    error_payload.update({"file": fname, "line": line_no})

                payload = {
                    "status": False,
                    "error": error_payload,
                    "time_spent": elapsed,
                }

                return json.dumps(payload) if return_json else payload

        return wrapper

    # --- Validate what type of decorator shall return
    if _func is None:  # That means using this type: @safe_execute()
        return decorator

    return decorator(func=_func)  # That means using this type: @safe_execute

