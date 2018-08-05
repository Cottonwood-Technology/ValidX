import pytest

from validateit import exc


def test_all_of(module):
    v = module.AllOf(module.Int(min=0), module.Int(max=10))
    assert v(1) == 1

    with pytest.raises(exc.MinValueError) as info:
        v(-1)
    assert info.value.context == [exc.StepNo(0)]
    assert info.value.expected == 0
    assert info.value.actual == -1

    with pytest.raises(exc.MaxValueError) as info:
        v(11)
    assert info.value.context == [exc.StepNo(1)]
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


def test_any_of(module):
    v = module.AnyOf(module.Int(options=[1, 2, 3]), module.Int(min=10))
    assert v(1) == 1
    assert v(2) == 2
    assert v(3) == 3
    assert v(10) == 10

    with pytest.raises(exc.SchemaError) as info:
        v(9)
    assert len(info.value.errors) == 2

    ne_1, ne_2 = info.value.errors

    assert isinstance(ne_1, exc.OptionsError)
    assert ne_1.context == [exc.StepNo(0)]
    assert ne_1.expected == [1, 2, 3]
    assert ne_1.actual == 9

    assert isinstance(ne_2, exc.MinValueError)
    assert ne_2.context == [exc.StepNo(1)]
    assert ne_2.expected == 10
    assert ne_2.actual == 9

    with pytest.raises(AssertionError) as info:
        module.AnyOf()
    assert info.value.args == ("At least one validation step has to be provided",)

    v = module.AnyOf(module.Int())
    v.steps = []
    with pytest.raises(AssertionError) as info:
        v(1)
    assert info.value.args == ("At least one validation step has to be passed",)
