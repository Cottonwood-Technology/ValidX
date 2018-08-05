import collections
import sys

import pytest
from webob.multidict import MultiDict as WebObMultiDict
from werkzeug.datastructures import MultiDict as WerkzeugMultiDict

from validateit import exc


if sys.version_info[0] < 3:
    str = unicode  # noqa


NoneType = type(None)


@pytest.fixture(params=["Dict", "Mapping"])
def dict_classes(module, request):
    yield module, getattr(module, request.param)


multidict_classes = [WebObMultiDict, WerkzeugMultiDict]
try:
    from multidict import MultiDict

    multidict_classes.append(MultiDict)
except ImportError:
    pass


class CustomMapping(collections.Mapping):
    def __init__(self, content):
        self.content = content

    def __getitem__(self, key):
        return self.content[key]

    def __iter__(self):
        return iter(self.content)

    def __len__(self):
        return len(self.content)


def test_dict(dict_classes):
    module, class_ = dict_classes
    v = class_({u"x": module.Int(), u"y": module.Int()})
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}
    assert v(collections.OrderedDict({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(collections.defaultdict(None, {u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}

    if class_.__name__ == "Mapping":
        assert v(CustomMapping({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(CustomMapping({u"x": 1, u"y": 2}))
        assert info.value.expected == dict
        assert info.value.actual == CustomMapping

    with pytest.raises(exc.InvalidTypeError) as info:
        v([(u"x", 1), (u"y", 2)])
    assert info.value.expected in (dict, collections.Mapping)
    assert info.value.actual == list

    with pytest.raises(exc.SchemaError) as info:
        v({u"x": u"1", u"y": None})
    assert len(info.value.errors) == 2

    ne_1, ne_2 = info.value.errors

    assert isinstance(ne_1, exc.InvalidTypeError)
    assert ne_1.context == [u"x"]
    assert ne_1.expected == int
    assert ne_1.actual == str

    assert isinstance(ne_2, exc.InvalidTypeError)
    assert ne_2.context == [u"y"]
    assert ne_2.expected == int
    assert ne_2.actual == NoneType


@pytest.mark.parametrize("nullable", [None, False, True])
def test_dict_nullable(dict_classes, nullable):
    module, class_ = dict_classes
    v = class_({u"x": module.Int(), u"y": module.Int()}, nullable=nullable)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected in (dict, collections.Mapping)
        assert info.value.actual == NoneType


@pytest.mark.parametrize("minlen", [None, 2])
@pytest.mark.parametrize("maxlen", [None, 3])
def test_dict_minlen_maxlen(dict_classes, minlen, maxlen):
    module, class_ = dict_classes
    v = class_(extra=(module.Str(), module.Int()), minlen=minlen, maxlen=maxlen)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}

    if minlen is None:
        assert v({u"x": 1}) == {u"x": 1}
    else:
        with pytest.raises(exc.MinLengthError) as info:
            v({u"x": 1})
        assert info.value.expected == minlen
        assert info.value.actual == 1

    if maxlen is None:
        assert v({u"x": 1, u"y": 2, u"z": 3, u"a": 4}) == {
            u"x": 1,
            u"y": 2,
            u"z": 3,
            u"a": 4,
        }
    else:
        with pytest.raises(exc.MaxLengthError) as info:
            v({u"x": 1, u"y": 2, u"z": 3, u"a": 4})
        assert info.value.expected == maxlen
        assert info.value.actual == 4


@pytest.mark.parametrize("defaults", [None, {u"x": 0}, {u"x": lambda: 0}])
@pytest.mark.parametrize("optional", [None, [u"x"]])
def test_dict_defaults_and_optional(dict_classes, defaults, optional):
    module, class_ = dict_classes
    v = class_(
        {u"x": module.Int(), u"y": module.Int()}, defaults=defaults, optional=optional
    )
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}

    with pytest.raises(exc.SchemaError) as info:
        v({u"x": 1})
    assert len(info.value.errors) == 1
    ne = info.value.errors[0]
    assert isinstance(ne, exc.MissingKeyError)
    assert ne.context == [u"y"]

    if defaults:
        assert v({u"y": 2}) == {u"x": 0, u"y": 2}
    elif optional:
        assert v({u"y": 2}) == {u"y": 2}
    else:
        with pytest.raises(exc.SchemaError) as info:
            v({u"y": 2})
        assert len(info.value.errors) == 1
        ne = info.value.errors[0]
        assert isinstance(ne, exc.MissingKeyError)
        assert ne.context == [u"x"]


@pytest.mark.parametrize("extra", [None, True])
def test_dict_extra(dict_classes, extra):
    module, class_ = dict_classes
    if extra:
        extra = (module.Str(), module.Int())
    v = class_({u"x": module.Int(), u"y": module.Int()}, extra=extra)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}

    if extra:
        assert v({u"x": 1, u"y": 2, u"z": 3}) == {u"x": 1, u"y": 2, u"z": 3}

        with pytest.raises(exc.SchemaError) as info:
            v({u"x": 1, u"y": 2, 3: None})
        assert len(info.value.errors) == 1

        ne = info.value.errors[0]

        assert isinstance(ne, exc.ExtraKeyError)
        assert ne.context == [3]

        assert isinstance(ne.key_error, exc.InvalidTypeError)
        assert ne.key_error.expected == str
        assert ne.key_error.actual == int

        assert isinstance(ne.value_error, exc.InvalidTypeError)
        assert ne.value_error.expected == int
        assert ne.value_error.actual == NoneType
    else:
        with pytest.raises(exc.SchemaError) as info:
            v({u"x": 1, u"y": 2, u"z": 3})
        assert len(info.value.errors) == 1
        ne = info.value.errors[0]
        assert isinstance(ne, exc.ForbiddenKeyError)
        assert ne.context == [u"z"]


@pytest.mark.parametrize("dispose", [None, [u"z"]])
def test_dict_dispose(dict_classes, dispose):
    module, class_ = dict_classes
    v = class_({u"x": module.Int(), u"y": module.Int()}, dispose=dispose)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}

    if dispose:
        assert v({u"x": 1, u"y": 2, u"z": 3}) == {u"x": 1, u"y": 2}
    else:
        with pytest.raises(exc.SchemaError) as info:
            v({u"x": 1, u"y": 2, u"z": 3})
        assert len(info.value.errors) == 1
        ne = info.value.errors[0]
        assert isinstance(ne, exc.ForbiddenKeyError)
        assert ne.context == [u"z"]


@pytest.mark.parametrize("multidict", multidict_classes)
def test_mapping_multikeys(module, multidict):
    v1 = module.Mapping({u"x": module.Int(), u"y": module.Int()})
    v2 = module.Mapping(
        {u"x": module.Int(), u"y": module.List(module.Int())}, multikeys=[u"y"]
    )
    data = multidict([(u"x", 1), (u"y", 2), (u"y", 3)])

    assert v1(data) == {u"x": 1, u"y": 3} or v1(data) == {u"x": 1, u"y": 2}
    assert v2(data) == {u"x": 1, u"y": [2, 3]}
