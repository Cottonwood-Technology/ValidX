import pytest

from validateit import py  # noqa

try:
    from validateit import cy  # noqa
except ImportError:
    pass


@pytest.fixture(params=[m for m in ("py", "cy") if m in globals()])
def module(request):
    result = globals()[request.param]
    yield result
    result.instances.clear()
