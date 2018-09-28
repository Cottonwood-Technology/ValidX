import pytest


@pytest.mark.benchmark(group="AllOf")
def test_all_of(module, benchmark):
    v = module.AllOf(module.Int(min=0), module.Int(max=10))
    assert benchmark(v, 1) == 1


# =============================================================================


@pytest.mark.benchmark(group="OneOf")
def test_any_of(module, benchmark):
    v = module.OneOf(module.Int(min=0), module.Int(min=10))
    assert benchmark(v, 1) == 1
