from collections import defaultdict, deque
from time import time

WINDOW_SECONDS = 300
_request_times = defaultdict(deque)
_failed_logins = defaultdict(deque)


def _cleanup(queue: deque, now: float) -> None:
    while queue and now - queue[0] > WINDOW_SECONDS:
        queue.popleft()


def record_request(ip: str) -> int:
    now = time()
    queue = _request_times[ip]
    queue.append(now)
    _cleanup(queue, now)
    return len(queue)


def record_failed_login(ip: str) -> int:
    now = time()
    queue = _failed_logins[ip]
    queue.append(now)
    _cleanup(queue, now)
    return len(queue)


def get_behavior(ip: str) -> dict:
    now = time()
    requests = _request_times[ip]
    failed = _failed_logins[ip]
    _cleanup(requests, now)
    _cleanup(failed, now)
    return {
        "requests_last_5m": len(requests),
        "failed_logins_last_5m": len(failed),
    }
