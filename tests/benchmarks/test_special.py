import pytest


@pytest.mark.benchmark(group="LazyRef")
def test_lazyref(module, benchmark):
    module.Int(alias="foo")
    v = module.LazyRef("foo")
    assert benchmark(v, 1) == 1


@pytest.mark.benchmark(group="LazyRef")
def test_lazyref_maxdepth(module, benchmark):
    v = module.Dict(
        {"x": module.Int(), "y": module.LazyRef("foo", maxdepth=10)},
        alias="foo",
        optional=("x", "y"),
    )
    data = {"y": {"y": {"y": {"y": {"y": {"y": {"x": 1}}}}}}}
    assert benchmark(v, data) == data


# =============================================================================


@pytest.mark.benchmark(group="Const")
def test_const(module, benchmark):
    v = module.Const(1)
    assert benchmark(v, 1) == 1


# =============================================================================


@pytest.mark.benchmark(group="Any")
def test_any(module, benchmark):
    v = module.Any()
    assert benchmark(v, 1) == 1


@pytest.mark.benchmark(group="Any")
def test_any_nullable(module, benchmark):
    v = module.Any(nullable=True)
    assert benchmark(v, None) is None
