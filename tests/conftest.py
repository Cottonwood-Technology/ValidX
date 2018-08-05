import pytest

from validateit import py, cy


@pytest.fixture(params=[py, cy])
def module(request):
    yield request.param
    request.param.instances.clear()
