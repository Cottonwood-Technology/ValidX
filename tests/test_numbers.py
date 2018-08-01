import math

import pytest

from validateit import py, cy
from validateit import exc


NoneType = type(None)
int_classes = [py.Int, cy.Int]
float_classes = [py.Float, cy.Float]


@pytest.mark.parametrize("class_", int_classes)
def test_int(class_):
    v = class_()
    assert v(5) == 5
    assert v(5.0) == 5


@pytest.mark.parametrize("class_", int_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_int_nullable(class_, nullable):
    v = class_(nullable=nullable)
    assert v(5) == 5

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == int
        assert info.value.actual == NoneType


@pytest.mark.parametrize("class_", int_classes)
@pytest.mark.parametrize("coerce", [None, False, True])
def test_int_coerce(class_, coerce):
    v = class_(coerce=coerce)
    assert v(5) == 5

    with pytest.raises(exc.InvalidTypeError) as info:
        v("abc")
    assert info.value.expected == int
    assert info.value.actual == str

    if coerce:
        assert v(5.5) == 5
        assert v("5") == 5
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(5.5)
        assert info.value.expected == int
        assert info.value.actual == float

        with pytest.raises(exc.InvalidTypeError) as info:
            v("5")
        assert info.value.expected == int
        assert info.value.actual == str


@pytest.mark.parametrize("class_", int_classes)
@pytest.mark.parametrize("min", [None, 0])
@pytest.mark.parametrize("max", [None, 10])
def test_int_min_max(class_, min, max):
    v = class_(min=min, max=max)
    assert v(5) == 5

    if min is None:
        assert v(-1) == -1
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(-1)
        assert info.value.expected == min
        assert info.value.actual == -1

    if max is None:
        assert v(11) == 11
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(11)
        assert info.value.expected == max
        assert info.value.actual == 11


@pytest.mark.parametrize("class_", int_classes)
@pytest.mark.parametrize("options", [None, [5, 6]])
def test_int_options(class_, options):
    v = class_(options=options)
    assert v(5) == 5
    assert v(6) == 6

    if options is None:
        assert v(4) == 4
    else:
        with pytest.raises(exc.OptionsError) as info:
            v(4)
        assert info.value.expected == options
        assert info.value.actual == 4


# =============================================================================


@pytest.mark.parametrize("class_", float_classes)
def test_float(class_):
    v = class_()
    assert v(5.5) == 5.5
    assert v(5) == 5.0


@pytest.mark.parametrize("class_", float_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_float_nullable(class_, nullable):
    v = class_(nullable=nullable)
    assert v(5.5) == 5.5

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == float
        assert info.value.actual == NoneType


@pytest.mark.parametrize("class_", float_classes)
@pytest.mark.parametrize("coerce", [None, False, True])
def test_float_coerce(class_, coerce):
    v = class_(coerce=coerce)
    assert v(5.5) == 5.5

    with pytest.raises(exc.InvalidTypeError) as info:
        v("abc")
    assert info.value.expected == float
    assert info.value.actual == str

    if coerce:
        assert v("5.5") == 5.5
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("5.5")
        assert info.value.expected == float
        assert info.value.actual == str


@pytest.mark.parametrize("class_", float_classes)
@pytest.mark.parametrize("nan", [None, False, True])
def test_float_nan(class_, nan):
    v = class_(nan=nan, coerce=True)
    assert v(5.5) == 5.5

    if nan:
        assert math.isnan(v("nan"))
    else:
        with pytest.raises(exc.FloatValueError) as info:
            v("nan")
        assert info.value.expected == "number"
        assert math.isnan(info.value.actual)


@pytest.mark.parametrize("class_", float_classes)
@pytest.mark.parametrize("inf", [None, False, True])
def test_float_inf(class_, inf):
    v = class_(inf=inf, coerce=True)
    assert v(5.5) == 5.5

    if inf:
        assert v("inf") == float("inf")
    else:
        with pytest.raises(exc.FloatValueError) as info:
            v("inf")
        assert info.value.expected == "finite"
        assert info.value.actual == float("inf")


@pytest.mark.parametrize("class_", float_classes)
@pytest.mark.parametrize("min", [None, 0])
@pytest.mark.parametrize("max", [None, 10])
def test_float_min_max(class_, min, max):
    v = class_(min=min, max=max)
    assert v(5.5) == 5.5

    if min is None:
        assert v(-1.5) == -1.5
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(-1.5)
        assert info.value.expected == min
        assert info.value.actual == -1.5

    if max is None:
        assert v(11.5) == 11.5
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(11.5)
        assert info.value.expected == max
        assert info.value.actual == 11.5
