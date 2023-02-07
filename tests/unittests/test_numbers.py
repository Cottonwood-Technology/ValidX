import math
import pickle
from decimal import Decimal

import pytest

from validx import exc


NoneType = type(None)


def test_int(module):
    v = module.Int()
    assert v(5) == 5
    assert v(5.0) == 5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v


@pytest.mark.parametrize("nullable", [None, False, True])
def test_int_nullable(module, nullable):
    v = module.Int(nullable=nullable)
    assert v(5) == 5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

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
    assert pickle.loads(pickle.dumps(v)) == v

    with pytest.raises(exc.InvalidTypeError) as info:
        v("abc")
    assert info.value.expected == int
    assert info.value.actual == str

    if coerce:
        assert v(5.5) == 5
        assert v("5") == 5
        assert v(True) == 1
        assert v(False) == 0
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(5.5)
        assert info.value.expected == int
        assert info.value.actual == float

        with pytest.raises(exc.InvalidTypeError) as info:
            v("5")
        assert info.value.expected == int
        assert info.value.actual == str

        with pytest.raises(exc.InvalidTypeError) as info:
            v(True)
        assert info.value.expected == int
        assert info.value.actual == bool


@pytest.mark.parametrize("min", [None, 0])
@pytest.mark.parametrize("max", [None, 10])
def test_int_min_max(module, min, max):
    v = module.Int(min=min, max=max)
    assert v(5) == 5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

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
    assert pickle.loads(pickle.dumps(v)) == v

    if options is None:
        assert v(4) == 4
    else:
        with pytest.raises(exc.OptionsError) as info:
            v(4)
        assert info.value.expected == frozenset(options)
        assert info.value.actual == 4


# =============================================================================


def test_float(module):
    v = module.Float()
    assert v(5.5) == 5.5
    assert v(5) == 5.0
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v


@pytest.mark.parametrize("nullable", [None, False, True])
def test_float_nullable(module, nullable):
    v = module.Float(nullable=nullable)
    assert v(5.5) == 5.5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

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
    assert pickle.loads(pickle.dumps(v)) == v

    with pytest.raises(exc.InvalidTypeError) as info:
        v("abc")
    assert info.value.expected == float
    assert info.value.actual == str

    if coerce:
        assert v("5.5") == 5.5
        assert v(True) == 1.0
        assert v(False) == 0.0
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("5.5")
        assert info.value.expected == float
        assert info.value.actual == str

        with pytest.raises(exc.InvalidTypeError) as info:
            v(True)
        assert info.value.expected == float
        assert info.value.actual == bool


@pytest.mark.parametrize("nan", [None, False, True])
def test_float_nan(module, nan):
    v = module.Float(nan=nan, coerce=True)
    assert v(5.5) == 5.5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if nan:
        assert math.isnan(v("nan"))
    else:
        with pytest.raises(exc.NumberError) as info:
            v("nan")
        assert info.value.expected == "number"
        assert math.isnan(info.value.actual)


@pytest.mark.parametrize("inf", [None, False, True])
def test_float_inf(module, inf):
    v = module.Float(inf=inf, coerce=True)
    assert v(5.5) == 5.5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if inf:
        assert v("inf") == float("inf")
    else:
        with pytest.raises(exc.NumberError) as info:
            v("inf")
        assert info.value.expected == "finite"
        assert info.value.actual == float("inf")


@pytest.mark.parametrize("min", [None, 0])
@pytest.mark.parametrize("max", [None, 10])
def test_float_min_max(module, min, max):
    v = module.Float(min=min, max=max, nan=True, inf=True)
    assert v(5.5) == 5.5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    assert math.isnan(v(float("nan")))

    if min is None:
        assert v(-1.5) == -1.5
        assert v(float("-inf")) == float("-inf")
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(-1.5)
        assert info.value.expected == min
        assert info.value.actual == -1.5

        with pytest.raises(exc.MinValueError) as info:
            v(float("-inf"))
        assert info.value.expected == min
        assert info.value.actual == float("-inf")

    if max is None:
        assert v(11.5) == 11.5
        assert v(float("inf")) == float("inf")
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(11.5)
        assert info.value.expected == max
        assert info.value.actual == 11.5

        with pytest.raises(exc.MaxValueError) as info:
            v(float("inf"))
        assert info.value.expected == max
        assert info.value.actual == float("inf")


# =============================================================================


def test_decimal(module):
    v = module.Decimal()
    assert v(Decimal("0.3")) == Decimal("0.3")
    assert v(0.3) == Decimal(0.3)
    assert v(0.3) != Decimal("0.3")
    assert v(1) == Decimal("1")
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v


@pytest.mark.parametrize("nullable", [None, False, True])
def test_decimal_nullable(module, nullable):
    v = module.Decimal(nullable=nullable)
    assert v(Decimal("0.3")) == Decimal("0.3")
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == Decimal
        assert info.value.actual == NoneType


@pytest.mark.parametrize("coerce", [None, False, True])
def test_decimal_coerce(module, coerce):
    v = module.Decimal(coerce=coerce)
    assert v(Decimal("0.3")) == Decimal("0.3")
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    with pytest.raises(exc.InvalidTypeError) as info:
        v("abc")
    assert info.value.expected == Decimal
    assert info.value.actual == str

    if coerce:
        assert v("5.5") == Decimal("5.5")
        assert v(True) == Decimal("1.0")
        assert v(False) == Decimal("0.0")
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("5.5")
        assert info.value.expected == Decimal
        assert info.value.actual == str

        with pytest.raises(exc.InvalidTypeError) as info:
            v(True)
        assert info.value.expected == Decimal
        assert info.value.actual == bool


@pytest.mark.parametrize("nan", [None, False, True])
def test_decimal_nan(module, nan):
    v = module.Decimal(nan=nan, coerce=True)
    assert v(Decimal("0.3")) == Decimal("0.3")
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if nan:
        assert v("NaN").is_nan()
    else:
        with pytest.raises(exc.NumberError) as info:
            v("NaN")
        assert info.value.expected == "number"
        assert math.isnan(info.value.actual)


@pytest.mark.parametrize("inf", [None, False, True])
def test_decimal_inf(module, inf):
    v = module.Decimal(inf=inf, coerce=True)
    assert v(Decimal("0.3")) == Decimal("0.3")
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if inf:
        assert v("Infinity") == Decimal("Infinity")
    else:
        with pytest.raises(exc.NumberError) as info:
            v("Infinity")
        assert info.value.expected == "finite"
        assert info.value.actual == Decimal("Infinity")


@pytest.mark.parametrize("min", [None, 0])
@pytest.mark.parametrize("max", [None, 10])
def test_decimal_min_max(module, min, max):
    v = module.Decimal(min=min, max=max, inf=True, nan=True)
    assert v(Decimal("0.3")) == Decimal("0.3")
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    assert v(Decimal("NaN")).is_nan()

    if min is None:
        assert v(Decimal("-1.5")) == Decimal("-1.5")
        assert v(Decimal("-Infinity")) == Decimal("-Infinity")
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(Decimal("-1.5"))
        assert info.value.expected == min
        assert info.value.actual == Decimal("-1.5")

        with pytest.raises(exc.MinValueError) as info:
            v(Decimal("-Infinity"))
        assert info.value.expected == min
        assert info.value.actual == Decimal("-Infinity")

    if max is None:
        assert v(Decimal("11.5")) == Decimal("11.5")
        assert v(Decimal("Infinity")) == Decimal("Infinity")
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(Decimal("11.5"))
        assert info.value.expected == max
        assert info.value.actual == Decimal("11.5")

        with pytest.raises(exc.MaxValueError) as info:
            v(Decimal("Infinity"))
        assert info.value.expected == max
        assert info.value.actual == Decimal("Infinity")


@pytest.mark.parametrize("precision", [None, 2])
def test_decimal_precision(module, precision):
    v = module.Decimal(precision=precision, inf=True, nan=True)
    assert v(Decimal("0.3")) == Decimal("0.3")
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if precision is None:
        assert v(Decimal("NaN")).is_nan()
        assert v(Decimal("Infinity")) == Decimal("Infinity")
        assert v(Decimal("0.001")) == Decimal("0.001")
        assert v(Decimal("0.043")) == Decimal("0.043")
        assert v(Decimal("0.045")) == Decimal("0.045")
        assert v(Decimal("0.5")) == Decimal("0.5")
    else:
        assert v(Decimal("NaN")).is_nan()
        assert v(Decimal("Infinity")) == Decimal("Infinity")
        assert v(Decimal("0.001")) == Decimal("0.00")
        assert v(Decimal("0.043")) == Decimal("0.04")
        assert v(Decimal("0.045")) == Decimal("0.05")
        assert v(Decimal("0.5")) == Decimal("0.50")
