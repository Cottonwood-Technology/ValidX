import pytest


@pytest.mark.benchmark(group="List")
def test_list(module, benchmark):
    v = module.List(module.Int())
    assert benchmark(v, [1, 2, 3]) == [1, 2, 3]


@pytest.mark.benchmark(group="List")
def test_list_nullable(module, benchmark):
    v = module.List(module.Int(), nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="List")
def test_list_minlen_maxlen(module, benchmark):
    v = module.List(module.Int(), minlen=2, maxlen=5)
    assert benchmark(v, [1, 2, 3]) == [1, 2, 3]


@pytest.mark.benchmark(group="List")
def test_list_unique(module, benchmark):
    v = module.List(module.Int(), unique=True)
    assert benchmark(v, [1, 2, 3, 3, 2, 1]) == [1, 2, 3]


# =============================================================================


@pytest.mark.benchmark(group="Tuple")
def test_tuple(module, benchmark):
    v = module.Tuple(module.Int(), module.Int())
    assert benchmark(v, (1, 2)) == (1, 2)


@pytest.mark.benchmark(group="Tuple")
def test_tuple_nullable(module, benchmark):
    v = module.Tuple(module.Int(), module.Int(), nullable=True)
    assert benchmark(v, None) is None
