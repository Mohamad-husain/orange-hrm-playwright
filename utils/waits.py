import re
import time


def wait_for_url_match(page, url_pattern, timeout_ms=30000):
    deadline = time.time() + (timeout_ms / 1000)

    while time.time() < deadline:
        if re.match(url_pattern, page.url):
            return
        page.wait_for_timeout(500)

    raise AssertionError(f"Expected URL matching {url_pattern}, got {page.url}")
