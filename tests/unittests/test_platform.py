from datetime import datetime, date

import pytest

from validx import platform


def test_min_and_max_timestamp():
    datetime.fromtimestamp(platform.MIN_TIMESTAMP)
    datetime.fromtimestamp(platform.MAX_TIMESTAMP)
    date.fromtimestamp(platform.MIN_TIMESTAMP)
    date.fromtimestamp(platform.MAX_TIMESTAMP)

    with pytest.raises((ValueError, OSError, OverflowError)):
        datetime.fromtimestamp(platform.MIN_TIMESTAMP - 1)

    with pytest.raises((ValueError, OSError, OverflowError)):
        datetime.fromtimestamp(platform.MAX_TIMESTAMP + 1)
