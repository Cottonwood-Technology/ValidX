import pytest

from validateit import py, cy  # noqa


@pytest.fixture(params=["py", "cy"])
def module(request):
    result = globals()[request.param]
    yield result
    result.instances.clear()
