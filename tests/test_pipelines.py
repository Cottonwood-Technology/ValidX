from collections import deque

import pytest

from validateit import exc


def test_all_of(module):
    v = module.AllOf(module.Int(min=0), module.Int(max=10))
    assert v(1) == 1
    assert v.clone() == v

    with pytest.raises(exc.MinValueError) as info:
        v(-1)
    assert info.value.context == deque([exc.Step(0)])
    assert info.value.expected == 0
    assert info.value.actual == -1

    with pytest.raises(exc.MaxValueError) as info:
        v(11)
    assert info.value.context == deque([exc.Step(1)])
    assert info.value.expected == 10
    assert info.value.actual == 11

    with pytest.raises(AssertionError) as info:
        module.AllOf()
    assert info.value.args == ("At least one validation step has to be provided",)

    v = module.AllOf(module.Int())
    v.steps = []
    with pytest.raises(AssertionError) as info:
        v(1)
    assert info.value.args == ("At least one validation step has to be passed",)


# =============================================================================


def test_any_of(module):
    v = module.OneOf(module.Int(options=[1, 2, 3]), module.Int(min=10))
    assert v(1) == 1
    assert v(2) == 2
    assert v(3) == 3
    assert v(10) == 10
    assert v.clone() == v

    with pytest.raises(exc.SchemaError) as info:
        v(9)
    assert len(info.value) == 2

    assert isinstance(info.value[0], exc.OptionsError)
    assert info.value[0].context == deque([exc.Step(0)])
    assert info.value[0].expected == [1, 2, 3]
    assert info.value[0].actual == 9

    assert isinstance(info.value[1], exc.MinValueError)
    assert info.value[1].context == deque([exc.Step(1)])
    assert info.value[1].expected == 10
    assert info.value[1].actual == 9

    with pytest.raises(AssertionError) as info:
        module.OneOf()
    assert info.value.args == ("At least one validation step has to be provided",)

    v = module.OneOf(module.Int())
    v.steps = []
    with pytest.raises(AssertionError) as info:
        v(1)
    assert info.value.args == ("At least one validation step has to be passed",)
