import sys
from collections import OrderedDict, defaultdict, deque

try:
    from collections.abc import Sequence, Mapping
except ImportError:
    from collections import Sequence, Mapping

import pytest

from webob.multidict import MultiDict as WebObMultiDict  # noqa
from werkzeug.datastructures import MultiDict as WerkzeugMultiDict  # noqa

try:
    from multidict import MultiDict  # noqa
except ImportError:
    pass

from validx import exc


if sys.version_info[0] < 3:
    str = unicode  # noqa


NoneType = type(None)


@pytest.fixture(
    params=[
        classname
        for classname in ("WebObMultiDict", "WerkzeugMultiDict", "MultiDict")
        if classname in globals()
    ]
)
def multidict_class(request):
    return globals()[request.param]


class CustomSequence(Sequence):
    def __init__(self, *items):
        self.items = items

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)


class CustomMapping(Mapping):
    def __init__(self, content):
        self.content = content

    def __getitem__(self, key):
        return self.content[key]

    def __iter__(self):
        return iter(self.content)

    def __len__(self):
        return len(self.content)


def test_list(module):
    v = module.List(module.Int())
    assert v([1, 2, 3]) == [1, 2, 3]
    assert v((1, 2, 3)) == [1, 2, 3]
    assert v(CustomSequence(1, 2, 3)) == [1, 2, 3]
    assert v.clone() == v

    with pytest.raises(exc.InvalidTypeError) as info:
        v(u"1, 2, 3")
    assert info.value.expected == Sequence
    assert info.value.actual == str

    with pytest.raises(exc.SchemaError) as info:
        v([1, u"2", 3, None])
    assert len(info.value) == 2

    assert isinstance(info.value[0], exc.InvalidTypeError)
    assert info.value[0].context == deque([1])
    assert info.value[0].expected == int
    assert info.value[0].actual == str

    assert isinstance(info.value[1], exc.InvalidTypeError)
    assert info.value[1].context == deque([3])
    assert info.value[1].expected == int
    assert info.value[1].actual == NoneType


@pytest.mark.parametrize("nullable", [None, False, True])
def test_list_nullable(module, nullable):
    v = module.List(module.Int(), nullable=nullable)
    assert v([1, 2, 3]) == [1, 2, 3]
    assert v((1, 2, 3)) == [1, 2, 3]
    assert v(CustomSequence(1, 2, 3)) == [1, 2, 3]
    assert v.clone() == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == Sequence
        assert info.value.actual == NoneType


@pytest.mark.parametrize("minlen", [None, 2])
@pytest.mark.parametrize("maxlen", [None, 5])
def test_list_minlen_maxlen(module, minlen, maxlen):
    v = module.List(module.Int(), minlen=minlen, maxlen=maxlen)
    assert v([1, 2, 3]) == [1, 2, 3]
    assert v((1, 2, 3)) == [1, 2, 3]
    assert v(CustomSequence(1, 2, 3)) == [1, 2, 3]
    assert v.clone() == v

    if minlen is None:
        assert v([1]) == [1]
    else:
        with pytest.raises(exc.MinLengthError) as info:
            v([1])
        assert info.value.expected == minlen
        assert info.value.actual == 1

    if maxlen is None:
        assert v([1, 2, 3, 4, 5, 6]) == [1, 2, 3, 4, 5, 6]
    else:
        with pytest.raises(exc.MaxLengthError) as info:
            v([1, 2, 3, 4, 5, 6])
        assert info.value.expected == maxlen
        assert info.value.actual == 6


@pytest.mark.parametrize("unique", [None, False, True])
def test_list_unique(module, unique):
    v = module.List(module.Int(), unique=unique)
    assert v([1, 2, 3]) == [1, 2, 3]
    assert v((1, 2, 3)) == [1, 2, 3]
    assert v(CustomSequence(1, 2, 3)) == [1, 2, 3]
    assert v.clone() == v

    if unique:
        assert v([1, 2, 3, 3, 2, 1]) == [1, 2, 3]
    else:
        assert v([1, 2, 3, 3, 2, 1]) == [1, 2, 3, 3, 2, 1]


# =============================================================================


def test_tuple(module):
    v = module.Tuple(module.Int(), module.Int())
    assert v([1, 2]) == (1, 2)
    assert v((1, 2)) == (1, 2)
    assert v(CustomSequence(1, 2)) == (1, 2)
    assert v.clone() == v

    with pytest.raises(exc.InvalidTypeError) as info:
        v(u"1, 2")
    assert info.value.expected == Sequence
    assert info.value.actual == str

    with pytest.raises(exc.TupleLengthError) as info:
        v([1, 2, 3])
    assert info.value.expected == 2
    assert info.value.actual == 3

    with pytest.raises(exc.SchemaError) as info:
        v([u"1", None])
    assert len(info.value) == 2

    assert isinstance(info.value[0], exc.InvalidTypeError)
    assert info.value[0].context == deque([0])
    assert info.value[0].expected == int
    assert info.value[0].actual == str

    assert isinstance(info.value[1], exc.InvalidTypeError)
    assert info.value[1].context == deque([1])
    assert info.value[1].expected == int
    assert info.value[1].actual == NoneType


@pytest.mark.parametrize("nullable", [None, False, True])
def test_tuple_nullable(module, nullable):
    v = module.Tuple(module.Int(), module.Int(), nullable=nullable)
    assert v([1, 2]) == (1, 2)
    assert v((1, 2)) == (1, 2)
    assert v(CustomSequence(1, 2)) == (1, 2)
    assert v.clone() == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == Sequence
        assert info.value.actual == NoneType


# =============================================================================


def test_dict(module):
    v = module.Dict({u"x": module.Int(), u"y": module.Int()})
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}
    assert v(OrderedDict({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(defaultdict(None, {u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(CustomMapping({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v.clone() == v

    with pytest.raises(exc.InvalidTypeError) as info:
        v([(u"x", 1), (u"y", 2)])
    assert info.value.expected == Mapping
    assert info.value.actual == list

    with pytest.raises(exc.SchemaError) as info:
        v({u"x": u"1", u"y": None})
    assert len(info.value) == 2

    info.value.sort()

    assert isinstance(info.value[0], exc.InvalidTypeError)
    assert info.value[0].context == deque([u"x"])
    assert info.value[0].expected == int
    assert info.value[0].actual == str

    assert isinstance(info.value[1], exc.InvalidTypeError)
    assert info.value[1].context == deque([u"y"])
    assert info.value[1].expected == int
    assert info.value[1].actual == NoneType


@pytest.mark.parametrize("nullable", [None, False, True])
def test_dict_nullable(module, nullable):
    v = module.Dict({u"x": module.Int(), u"y": module.Int()}, nullable=nullable)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}
    assert v(OrderedDict({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(defaultdict(None, {u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(CustomMapping({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v.clone() == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == Mapping
        assert info.value.actual == NoneType


@pytest.mark.parametrize("minlen", [None, 2])
@pytest.mark.parametrize("maxlen", [None, 3])
def test_dict_minlen_maxlen(module, minlen, maxlen):
    v = module.Dict(extra=(module.Str(), module.Int()), minlen=minlen, maxlen=maxlen)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}
    assert v(OrderedDict({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(defaultdict(None, {u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(CustomMapping({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v.clone() == v

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
def test_dict_defaults_and_optional(module, defaults, optional):
    v = module.Dict(
        {u"x": module.Int(), u"y": module.Int()}, defaults=defaults, optional=optional
    )
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}
    assert v(OrderedDict({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(defaultdict(None, {u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(CustomMapping({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v.clone() == v

    with pytest.raises(exc.SchemaError) as info:
        v({u"x": 1})
    assert len(info.value) == 1
    assert isinstance(info.value[0], exc.MissingKeyError)
    assert info.value[0].context == deque([u"y"])

    if defaults:
        assert v({u"y": 2}) == {u"x": 0, u"y": 2}
    elif optional:
        assert v({u"y": 2}) == {u"y": 2}
    else:
        with pytest.raises(exc.SchemaError) as info:
            v({u"y": 2})
        assert len(info.value) == 1
        assert isinstance(info.value[0], exc.MissingKeyError)
        assert info.value[0].context == deque([u"x"])


@pytest.mark.parametrize("extra", [None, True])
def test_dict_extra(module, extra):
    if extra:
        extra = (module.Str(), module.Int())
    v = module.Dict({u"x": module.Int(), u"y": module.Int()}, extra=extra)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}
    assert v(OrderedDict({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(defaultdict(None, {u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(CustomMapping({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v.clone() == v

    if extra:
        assert v({u"x": 1, u"y": 2, u"z": 3}) == {u"x": 1, u"y": 2, u"z": 3}

        with pytest.raises(exc.SchemaError) as info:
            v({u"x": 1, u"y": 2, 3: None})
        assert len(info.value) == 2

        info.value.sort()

        assert isinstance(info.value[0], exc.InvalidTypeError)
        assert info.value[0].context == deque([3, exc.EXTRA_KEY])
        assert info.value[0].expected == str
        assert info.value[0].actual == int

        assert isinstance(info.value[1], exc.InvalidTypeError)
        assert info.value[1].context == deque([3, exc.EXTRA_VALUE])
        assert info.value[1].expected == int
        assert info.value[1].actual == NoneType
    else:
        with pytest.raises(exc.SchemaError) as info:
            v({u"x": 1, u"y": 2, u"z": 3})
        assert len(info.value) == 1
        assert isinstance(info.value[0], exc.ForbiddenKeyError)
        assert info.value[0].context == deque([u"z"])


@pytest.mark.parametrize("dispose", [None, [u"z"]])
def test_dict_dispose(module, dispose):
    v = module.Dict({u"x": module.Int(), u"y": module.Int()}, dispose=dispose)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}
    assert v(OrderedDict({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(defaultdict(None, {u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(CustomMapping({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v.clone() == v

    if dispose:
        assert v({u"x": 1, u"y": 2, u"z": 3}) == {u"x": 1, u"y": 2}
    else:
        with pytest.raises(exc.SchemaError) as info:
            v({u"x": 1, u"y": 2, u"z": 3})
        assert len(info.value) == 1
        assert isinstance(info.value[0], exc.ForbiddenKeyError)
        assert info.value[0].context == deque([u"z"])


def test_dict_multikeys(module, multidict_class):
    v1 = module.Dict({u"x": module.Int(), u"y": module.Int()})
    v2 = module.Dict(
        {u"x": module.Int(), u"y": module.List(module.Int())}, multikeys=[u"y"]
    )
    data = multidict_class([(u"x", 1), (u"y", 2), (u"y", 3)])

    assert v1(data) == {u"x": 1, u"y": 3} or v1(data) == {u"x": 1, u"y": 2}
    assert v2(data) == {u"x": 1, u"y": [2, 3]}
    assert v1.clone() == v1
    assert v2.clone() == v2
