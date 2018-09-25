import pytest


@pytest.fixture(params=["Dict", "Mapping"])
def dict_classes(module, request):
    yield module, getattr(module, request.param)


@pytest.mark.benchmark(group="Dict")
def test_dict(dict_classes, benchmark):
    module, class_ = dict_classes
    v = class_({u"x": module.Int(), u"y": module.Int()})
    assert benchmark(v, {u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}


@pytest.mark.benchmark(group="Dict")
def test_dict_nullable(dict_classes, benchmark):
    module, class_ = dict_classes
    v = class_({u"x": module.Int(), u"y": module.Int()}, nullable=True)
    assert benchmark(v, None) is None


@pytest.mark.benchmark(group="Dict")
def test_dict_minlen_maxlen(dict_classes, benchmark):
    module, class_ = dict_classes
    v = class_(extra=(module.Str(), module.Int()), minlen=2, maxlen=3)
    assert benchmark(v, {u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}


@pytest.mark.benchmark(group="Dict")
def test_dict_defaults(dict_classes, benchmark):
    module, class_ = dict_classes
    v = class_({u"x": module.Int(), u"y": module.Int()}, defaults={u"x": 1})
    assert benchmark(v, {u"y": 2}) == {u"x": 1, u"y": 2}


@pytest.mark.benchmark(group="Dict")
def test_dict_optional(dict_classes, benchmark):
    module, class_ = dict_classes
    v = class_({u"x": module.Int(), u"y": module.Int()}, optional=(u"x",))
    assert benchmark(v, {u"y": 2}) == {u"y": 2}


@pytest.mark.benchmark(group="Dict")
def test_dict_extra(dict_classes, benchmark):
    module, class_ = dict_classes
    v = class_(
        {u"x": module.Int(), u"y": module.Int()}, extra=(module.Str(), module.Int())
    )
    assert benchmark(v, {u"x": 1, u"y": 2, u"z": 3}) == {u"x": 1, u"y": 2, u"z": 3}


@pytest.mark.benchmark(group="Dict")
def test_dict_dispose(dict_classes, benchmark):
    module, class_ = dict_classes
    v = class_({u"x": module.Int(), u"y": module.Int()}, dispose=(u"z",))
    assert benchmark(v, {u"x": 1, u"y": 2, u"z": 3}) == {u"x": 1, u"y": 2}
