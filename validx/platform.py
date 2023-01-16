from datetime import datetime


__all__ = ["MIN_TIMESTAMP", "MAX_TIMESTAMP"]


def get_min_timestamp():
    """Calculate minimal supported timestamp value on current platform"""
    result = 0
    delta = 1 << 32
    while delta:
        approximation = result - delta
        try:
            datetime.fromtimestamp(approximation)
        except (ValueError, OSError, OverflowError):
            delta >>= 1
        else:
            result = approximation
    return result


def get_max_timestamp():
    """Calculate maximal supported timestamp value on current platform"""
    result = 0
    delta = 1 << 32
    while delta:
        approximation = result + delta
        try:
            datetime.fromtimestamp(approximation)
        except (ValueError, OSError, OverflowError):
            delta >>= 1
        else:
            result = approximation
    return result


MIN_TIMESTAMP = get_min_timestamp()
MAX_TIMESTAMP = get_max_timestamp()
