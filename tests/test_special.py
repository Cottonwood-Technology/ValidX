import pytest

from validateit import py, cy
from validateit import exc


NoneType = type(None)
any_classes = [py.Any, cy.Any]


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


@pytest.mark.parametrize("class_", any_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_any(class_, nullable):
    v = class_(nullable=nullable)
    assert v(True) is True
    assert v(1) == 1
    assert v("x") == "x"
    assert v([1, "x"]) == [1, "x"]

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == object
        assert info.value.actual == NoneType
