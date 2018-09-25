import math

import pytest


@pytest.mark.benchmark(group="Int")
def test_int(module, benchmark):
    v = module.Int()
    assert benchmark(v, 5) == 5


@pytest.mark.benchmark(group="Int")
def test_int_nullable(module, benchmark):
    v = module.Int(nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="Int")
def test_int_coerce(module, benchmark):
    v = module.Int(coerce=True)
    assert benchmark(v, "5") == 5


@pytest.mark.benchmark(group="Int")
def test_int_float_coerce(module, benchmark):
    v = module.Int()
    assert benchmark(v, 5.0) == 5


@pytest.mark.benchmark(group="Int")
def test_int_min_max(module, benchmark):
    v = module.Int(min=1, max=10)
    assert benchmark(v, 5) == 5


@pytest.mark.benchmark(group="Int")
def test_int_options(module, benchmark):
    v = module.Int(options=(3, 4, 5, 6, 7))
    assert benchmark(v, 5) == 5


# =============================================================================


@pytest.mark.benchmark(group="Float")
def test_float(module, benchmark):
    v = module.Float()
    assert benchmark(v, 5.5) == 5.5


@pytest.mark.benchmark(group="Float")
def test_float_nullable(module, benchmark):
    v = module.Float(nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="Float")
def test_float_coerce(module, benchmark):
    v = module.Float(coerce=True)
    assert benchmark(v, "5.5") == 5.5


@pytest.mark.benchmark(group="Float")
def test_float_int_coerce(module, benchmark):
    v = module.Float()
    assert benchmark(v, 5) == 5.0


@pytest.mark.benchmark(group="Float")
def test_float_nan(module, benchmark):
    v = module.Float(nan=True)
    result = benchmark(v, float("nan"))
    assert math.isnan(result)


@pytest.mark.benchmark(group="Float")
def test_float_inf(module, benchmark):
    v = module.Float(inf=True)
    assert benchmark(v, float("inf")) == float("inf")


@pytest.mark.benchmark(group="Float")
def test_float_min_max(module, benchmark):
    v = module.Float(min=1.0, max=10.0)
    assert benchmark(v, 5.5) == 5.5
