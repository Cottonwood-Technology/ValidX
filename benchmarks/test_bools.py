import pytest


@pytest.mark.benchmark(group="Bool")
def test_bool(module, benchmark):
    v = module.Bool()
    assert benchmark(v, True) is True


@pytest.mark.benchmark(group="Bool")
def test_bool_nullable(module, benchmark):
    v = module.Bool(nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="Bool")
def test_bool_coerce_str(module, benchmark):
    v = module.Bool(coerce_str=True)
    assert benchmark(v, "On") is True


@pytest.mark.benchmark(group="Bool")
def test_bool_coerce_int(module, benchmark):
    v = module.Bool(coerce_int=True)
    assert benchmark(v, 1) is True
