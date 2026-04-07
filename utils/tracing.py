import re
from functools import wraps
from pathlib import Path


TRACE_DIR = Path(".playwright-traces")


def _trace_path(node_id: str) -> Path:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", node_id).strip("._")
    return TRACE_DIR / f"{safe_name or 'trace'}.zip"


def playwright_trace(page_fixture_name: str = "page"):
    """Capture a Playwright trace for decorated tests when they fail."""

    def decorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            page = kwargs.get(page_fixture_name)
            if page is None:
                raise RuntimeError(
                    f"Missing '{page_fixture_name}' fixture required by playwright_trace"
                )

            request = kwargs.get("request")
            trace_name = request.node.nodeid if request else test_func.__name__
            trace_path = _trace_path(trace_name)
            TRACE_DIR.mkdir(parents=True, exist_ok=True)

            page.context.tracing.start(
                screenshots=True,
                snapshots=True,
                sources=True,
            )
            try:
                return test_func(*args, **kwargs)
            except Exception:
                page.context.tracing.stop(path=str(trace_path))
                raise
            else:
                page.context.tracing.stop()

        return wrapper

    return decorator
