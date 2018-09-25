import pytest


@pytest.fixture(params=["LazyRef", "LazyRefTS"])
def lazyref_classes(module, request):
    yield module, getattr(module, request.param)


@pytest.mark.benchmark(group="LazyRef")
def test_lazyref(lazyref_classes, benchmark):
    module, class_ = lazyref_classes
    module.Int(alias="foo")
    v = class_("foo")
    assert benchmark(v, 1) == 1


@pytest.mark.benchmark(group="LazyRef")
def test_lazyref_maxdepth(lazyref_classes, benchmark):
    module, class_ = lazyref_classes
    module.Int(alias="foo")
    v = class_("foo", maxdepth=2)
    assert benchmark(v, 1) == 1


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
