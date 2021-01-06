import pytest


@pytest.mark.benchmark(group="Str")
def test_str(module, benchmark):
    v = module.Str()
    assert benchmark(v, "abc") == "abc"


@pytest.mark.benchmark(group="Str")
def test_str_nullable(module, benchmark):
    v = module.Str(nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="Str")
def test_str_encoding(module, benchmark):
    v = module.Str(encoding="utf-8")
    assert benchmark(v, b"abc") == "abc"


@pytest.mark.benchmark(group="Str")
def test_str_minlen_maxlen(module, benchmark):
    v = module.Str(minlen=1, maxlen=10)
    assert benchmark(v, "abc") == "abc"


@pytest.mark.benchmark(group="Str")
def test_str_pattern(module, benchmark):
    v = module.Str(pattern="(?i)^[a-z]+$")
    assert benchmark(v, "abc") == "abc"


@pytest.mark.benchmark(group="Str")
def test_str_options(module, benchmark):
    v = module.Str(options=("abc", "xyz"))
    assert benchmark(v, "abc") == "abc"


# =============================================================================


@pytest.mark.benchmark(group="Bytes")
def test_bytes(module, benchmark):
    v = module.Bytes()
    assert benchmark(v, b"abc") == b"abc"


@pytest.mark.benchmark(group="Bytes")
def test_bytes_nullable(module, benchmark):
    v = module.Bytes(nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="Bytes")
def test_bytes_minlen_maxlen(module, benchmark):
    v = module.Bytes(minlen=1, maxlen=10)
    assert benchmark(v, b"abc") == b"abc"
