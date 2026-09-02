import functools
import logging
import time

import requests

logger = logging.getLogger(__name__)


def retry_with_backoff(retries=3, base_delay=1.0):
    # only retries connection-level failures, not auth or bad response
    # errors, those aren't going to fix themselves by waiting
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as exc:
                    attempt += 1
                    if attempt >= retries:
                        raise
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(
                        "%s failed (attempt %d/%d): %s. retrying in %.1fs",
                        func.__name__, attempt, retries, exc, delay,
                    )
                    time.sleep(delay)

        return wrapper

    return decorator
