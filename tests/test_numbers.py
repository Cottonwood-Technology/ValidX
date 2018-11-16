import math

import pytest

from validx import exc


NoneType = type(None)


def test_int(module):
    v = module.Int()
    assert v(5) == 5
    assert v(5.0) == 5
    assert v.clone() == v


@pytest.mark.parametrize("nullable", [None, False, True])
def test_int_nullable(module, nullable):
    v = module.Int(nullable=nullable)
    assert v(5) == 5
    assert v.clone() == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == int
        assert info.value.actual == NoneType


@pytest.mark.parametrize("coerce", [None, False, True])
def test_int_coerce(module, coerce):
    v = module.Int(coerce=coerce)
    assert v(5) == 5
    assert v.clone() == v

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


@pytest.mark.parametrize("min", [None, 0])
@pytest.mark.parametrize("max", [None, 10])
def test_int_min_max(module, min, max):
    v = module.Int(min=min, max=max)
    assert v(5) == 5
    assert v.clone() == v

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


@pytest.mark.parametrize("options", [None, [5, 6]])
def test_int_options(module, options):
    v = module.Int(options=options)
    assert v(5) == 5
    assert v(6) == 6
    assert v.clone() == v

    if options is None:
        assert v(4) == 4
    else:
        with pytest.raises(exc.OptionsError) as info:
            v(4)
        assert info.value.expected == options
        assert info.value.actual == 4


# =============================================================================


def test_float(module):
    v = module.Float()
    assert v(5.5) == 5.5
    assert v(5) == 5.0
    assert v.clone() == v


@pytest.mark.parametrize("nullable", [None, False, True])
def test_float_nullable(module, nullable):
    v = module.Float(nullable=nullable)
    assert v(5.5) == 5.5
    assert v.clone() == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == float
        assert info.value.actual == NoneType


@pytest.mark.parametrize("coerce", [None, False, True])
def test_float_coerce(module, coerce):
    v = module.Float(coerce=coerce)
    assert v(5.5) == 5.5
    assert v.clone() == v

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


@pytest.mark.parametrize("nan", [None, False, True])
def test_float_nan(module, nan):
    v = module.Float(nan=nan, coerce=True)
    assert v(5.5) == 5.5
    assert v.clone() == v

    if nan:
        assert math.isnan(v("nan"))
    else:
        with pytest.raises(exc.FloatValueError) as info:
            v("nan")
        assert info.value.expected == "number"
        assert math.isnan(info.value.actual)


@pytest.mark.parametrize("inf", [None, False, True])
def test_float_inf(module, inf):
    v = module.Float(inf=inf, coerce=True)
    assert v(5.5) == 5.5
    assert v.clone() == v

    if inf:
        assert v("inf") == float("inf")
    else:
        with pytest.raises(exc.FloatValueError) as info:
            v("inf")
        assert info.value.expected == "finite"
        assert info.value.actual == float("inf")


@pytest.mark.parametrize("min", [None, 0])
@pytest.mark.parametrize("max", [None, 10])
def test_float_min_max(module, min, max):
    v = module.Float(min=min, max=max)
    assert v(5.5) == 5.5
    assert v.clone() == v

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
