import collections
import sys

try:
    import typing as t  # noqa
except ImportError:
    pass

import pytest  # type: ignore

from validateit import py, cy
from validateit import exc


if sys.version_info[0] < 3:
    str = unicode  # noqa


NoneType = type(None)
list_classes = [py.List, py.Sequence, cy.List, cy.Sequence]
tuple_classes = [py.Tuple, cy.Tuple]


class CustomSequence(collections.Sequence):
    def __init__(self, *items):
        self.items = items

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)


@pytest.mark.parametrize("class_", list_classes)
def test_list(class_):
    # type: (t.Type[py.List]) -> None
    v = class_(py.Int())
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
    assert ne_2.actual == NoneType  # type: ignore


@pytest.mark.parametrize("class_", list_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_list_nullable(class_, nullable):
    # type: (t.Type[py.List], t.Optional[bool]) -> None
    v = class_(py.Int(), nullable=nullable)
    assert v([1, 2, 3]) == [1, 2, 3]
    assert v((1, 2, 3)) == [1, 2, 3]

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected in ((list, tuple), collections.Sequence)
        assert info.value.actual == NoneType  # type: ignore


@pytest.mark.parametrize("class_", list_classes)
@pytest.mark.parametrize("minlen", [None, 2])
@pytest.mark.parametrize("maxlen", [None, 5])
def test_list_minlen_maxlen(class_, minlen, maxlen):
    # type: (t.Type[py.List], t.Optional[int], t.Optional[int]) -> None
    v = class_(py.Int(), minlen=minlen, maxlen=maxlen)
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


@pytest.mark.parametrize("class_", list_classes)
@pytest.mark.parametrize("unique", [None, False, True])
def test_list_unique(class_, unique):
    # type: (t.Type[py.List], t.Optional[bool]) -> None
    v = class_(py.Int(), unique=unique)
    assert v([1, 2, 3]) == [1, 2, 3]
    assert v((1, 2, 3)) == [1, 2, 3]

    if unique:
        assert v([1, 2, 3, 3, 2, 1]) == [1, 2, 3]
    else:
        assert v([1, 2, 3, 3, 2, 1]) == [1, 2, 3, 3, 2, 1]


# =============================================================================


@pytest.mark.parametrize("class_", tuple_classes)
def test_tuple(class_):
    # type: (t.Type[py.Tuple]) -> None
    v = class_(py.Int(), py.Int())
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
    assert ne_2.actual == NoneType  # type: ignore


@pytest.mark.parametrize("class_", tuple_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_tuple_nullable(class_, nullable):
    # type: (t.Type[py.Tuple], t.Optional[bool]) -> None
    v = class_(py.Int(), py.Int(), nullable=nullable)
    assert v([1, 2]) == (1, 2)
    assert v((1, 2)) == (1, 2)

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == (list, tuple)
        assert info.value.actual == NoneType  # type: ignore
