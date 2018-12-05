from datetime import datetime

from validx import util


def test_utc():
    assert repr(util.UTC) == "<UTC>"
    assert datetime.now(util.UTC).strftime("%Z") == "UTC"
