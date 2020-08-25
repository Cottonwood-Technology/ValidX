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


# =============================================================================


@pytest.mark.benchmark(group="Dict")
def test_dict(module, benchmark):
    v = module.Dict({u"x": module.Int(), u"y": module.Int()})
    assert benchmark(v, {u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}


@pytest.mark.benchmark(group="Dict")
def test_dict_nullable(module, benchmark):
    v = module.Dict({u"x": module.Int(), u"y": module.Int()}, nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="Dict")
def test_dict_minlen_maxlen(module, benchmark):
    v = module.Dict(extra=(module.Str(), module.Int()), minlen=2, maxlen=3)
    assert benchmark(v, {u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}


@pytest.mark.benchmark(group="Dict")
def test_dict_defaults(module, benchmark):
    v = module.Dict({u"x": module.Int(), u"y": module.Int()}, defaults={u"x": 1})
    assert benchmark(v, {u"y": 2}) == {u"x": 1, u"y": 2}


@pytest.mark.benchmark(group="Dict")
def test_dict_optional(module, benchmark):
    v = module.Dict({u"x": module.Int(), u"y": module.Int()}, optional=(u"x",))
    assert benchmark(v, {u"y": 2}) == {u"y": 2}


@pytest.mark.benchmark(group="Dict")
def test_dict_extra(module, benchmark):
    v = module.Dict(
        {u"x": module.Int(), u"y": module.Int()}, extra=(module.Str(), module.Int())
    )
    assert benchmark(v, {u"x": 1, u"y": 2, u"z": 3}) == {u"x": 1, u"y": 2, u"z": 3}


@pytest.mark.benchmark(group="Dict")
def test_dict_dispose(module, benchmark):
    v = module.Dict({u"x": module.Int(), u"y": module.Int()}, dispose=(u"z",))
    assert benchmark(v, {u"x": 1, u"y": 2, u"z": 3}) == {u"x": 1, u"y": 2}
