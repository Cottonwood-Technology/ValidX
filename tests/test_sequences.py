import collections
import sys

import pytest

from validateit import exc


if sys.version_info[0] < 3:
    str = unicode  # noqa


NoneType = type(None)


@pytest.fixture(params=["List", "Sequence"])
def list_classes(module, request):
    yield module, getattr(module, request.param)


class CustomSequence(collections.Sequence):
    def __init__(self, *items):
        self.items = items

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)


def test_list(list_classes):
    module, class_ = list_classes
    v = class_(module.Int())
    assert v([1, 2, 3]) == [1, 2, 3]
    assert v((1, 2, 3)) == [1, 2, 3]

    if class_.__name__ == "Sequence":
        assert v(CustomSequence(1, 2, 3)) == [1, 2, 3]
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(CustomSequence(1, 2, 3))
        assert info.value.expected == (list, tuple)
        assert info.value.actual == CustomSequence

    with pytest.raises(exc.InvalidTypeError) as info:
        v(u"1, 2, 3")
    assert info.value.expected in ((list, tuple), collections.Sequence)
    assert info.value.actual == str

    with pytest.raises(exc.SchemaError) as info:
        v([1, u"2", 3, None])
    assert len(info.value.errors) == 2

    ne_1, ne_2 = info.value.errors

    assert isinstance(ne_1, exc.InvalidTypeError)
    assert ne_1.context == [1]
    assert ne_1.expected == int
    assert ne_1.actual == str

    assert isinstance(ne_2, exc.InvalidTypeError)
    assert ne_2.context == [3]
    assert ne_2.expected == int
    assert ne_2.actual == NoneType


@pytest.mark.parametrize("nullable", [None, False, True])
def test_list_nullable(list_classes, nullable):
    module, class_ = list_classes
    v = class_(module.Int(), nullable=nullable)
    assert v([1, 2, 3]) == [1, 2, 3]
    assert v((1, 2, 3)) == [1, 2, 3]

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected in ((list, tuple), collections.Sequence)
        assert info.value.actual == NoneType


@pytest.mark.parametrize("minlen", [None, 2])
@pytest.mark.parametrize("maxlen", [None, 5])
def test_list_minlen_maxlen(list_classes, minlen, maxlen):
    module, class_ = list_classes
    v = class_(module.Int(), minlen=minlen, maxlen=maxlen)
    assert v([1, 2, 3]) == [1, 2, 3]
    assert v((1, 2, 3)) == [1, 2, 3]

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
def test_list_unique(list_classes, unique):
    module, class_ = list_classes
    v = class_(module.Int(), unique=unique)
    assert v([1, 2, 3]) == [1, 2, 3]
    assert v((1, 2, 3)) == [1, 2, 3]

    if unique:
        assert v([1, 2, 3, 3, 2, 1]) == [1, 2, 3]
    else:
        assert v([1, 2, 3, 3, 2, 1]) == [1, 2, 3, 3, 2, 1]


# =============================================================================


def test_tuple(module):
    v = module.Tuple(module.Int(), module.Int())
    assert v([1, 2]) == (1, 2)
    assert v((1, 2)) == (1, 2)

    with pytest.raises(exc.InvalidTypeError) as info:
        v(u"1, 2")
    assert info.value.expected == (list, tuple)
    assert info.value.actual == str

    with pytest.raises(exc.TupleLengthError) as info:
        v([1, 2, 3])
    assert info.value.expected == 2
    assert info.value.actual == 3

    with pytest.raises(exc.SchemaError) as info:
        v([u"1", None])
    assert len(info.value.errors) == 2

    ne_1, ne_2 = info.value.errors

    assert isinstance(ne_1, exc.InvalidTypeError)
    assert ne_1.context == [0]
    assert ne_1.expected == int
    assert ne_1.actual == str

    assert isinstance(ne_2, exc.InvalidTypeError)
    assert ne_2.context == [1]
    assert ne_2.expected == int
    assert ne_2.actual == NoneType


@pytest.mark.parametrize("nullable", [None, False, True])
def test_tuple_nullable(module, nullable):
    v = module.Tuple(module.Int(), module.Int(), nullable=nullable)
    assert v([1, 2]) == (1, 2)
    assert v((1, 2)) == (1, 2)

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == (list, tuple)
        assert info.value.actual == NoneType
