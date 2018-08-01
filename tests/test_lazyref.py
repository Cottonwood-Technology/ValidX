import pytest

from validateit import py, cy
from validateit import exc


@pytest.fixture(params=[py, cy])
def module(request):
    yield request.param
    request.param.instances.clear()


def test_lazyref(module):
    v = module.Dict(
        {"x": module.Int(), "y": module.LazyRef("foo", maxdepth=2)},
        alias="foo",
        optional=["x", "y"],
    )

    data = {"x": 1}
    assert v(data) == data

    data = {"y": {"x": 1}}
    assert v(data) == data

    data = {"y": {"y": {"x": 1}}}
    assert v(data) == data

    with pytest.raises(exc.SchemaError) as info:
        v({"y": {"y": {"y": {"x": 1}}}})
    assert len(info.value.errors) == 1

    ne = info.value.errors[0]

    assert isinstance(ne, exc.RecursionMaxDepthError)
    assert ne.context == ["y", "y", "y"]
    assert ne.expected == 2
    assert ne.actual == 3
