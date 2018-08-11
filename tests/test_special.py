from collections import deque

import pytest

from validateit import exc


NoneType = type(None)


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
    assert len(info.value) == 1

    assert isinstance(info.value[0], exc.RecursionMaxDepthError)
    assert info.value[0].context == deque(["y", "y", "y"])
    assert info.value[0].expected == 2
    assert info.value[0].actual == 3


def test_const(module):
    v = module.Const(1)
    assert v(1) == 1

    with pytest.raises(exc.OptionsError) as info:
        v(2)
    assert info.value.expected == [1]
    assert info.value.actual == 2


@pytest.mark.parametrize("nullable", [None, False, True])
def test_any(module, nullable):
    v = module.Any(nullable=nullable)
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
