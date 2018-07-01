# coding: utf-8

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
str_classes = [py.Str, cy.Str]
bytes_classes = [py.Bytes, cy.Bytes]


@pytest.mark.parametrize("class_", str_classes)
def test_str(class_):
    # type: (t.Type[py.Str]) -> None
    v = class_()
    assert v(u"abc") == u"abc"


@pytest.mark.parametrize("class_", str_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_str_nullable(class_, nullable):
    # type: (t.Type[py.Str], t.Optional[bool]) -> None
    v = class_(nullable=nullable)
    assert v(u"abc") == u"abc"

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == str
        assert info.value.actual == NoneType


@pytest.mark.parametrize("class_", str_classes)
@pytest.mark.parametrize("encoding", [None, "utf-8"])
def test_str_encoding(class_, encoding):
    # type: (t.Type[py.Str], t.Optional[str]) -> None
    v = class_(encoding=encoding)
    assert v(u"abc") == u"abc"

    if encoding:
        assert v(b"abc") == u"abc"

        error = u"café".encode("latin-1")
        with pytest.raises(exc.StrDecodeError) as info:
            v(error)
        assert info.value.expected == encoding
        assert info.value.actual == error
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(b"abc")
        assert info.value.expected == str
        assert info.value.actual == bytes


@pytest.mark.parametrize("class_", str_classes)
@pytest.mark.parametrize("minlen", [None, 2])
@pytest.mark.parametrize("maxlen", [None, 5])
def test_str_minlen_maxlen(class_, minlen, maxlen):
    # type: (t.Type[py.Str], t.Optional[int], t.Optional[int]) -> None
    v = class_(minlen=minlen, maxlen=maxlen)
    assert v(u"abc") == u"abc"

    if minlen is None:
        assert v(u"a") == u"a"
    else:
        with pytest.raises(exc.MinLengthError) as info:
            v(u"a")
        assert info.value.expected == minlen
        assert info.value.actual == 1

    if maxlen is None:
        assert v(u"abcdef") == u"abcdef"
    else:
        with pytest.raises(exc.MaxLengthError) as info:
            v(u"abcdef")
        assert info.value.expected == maxlen
        assert info.value.actual == 6


@pytest.mark.parametrize("class_", str_classes)
@pytest.mark.parametrize("pattern", [None, u"^(?i)[a-z]+$"])
def test_str_pattern(class_, pattern):
    # type: (t.Type[py.Str], t.Optional[str]) -> None
    v = class_(pattern=pattern)
    assert v(u"abc") == u"abc"
    assert v(u"ABC") == u"ABC"

    if pattern is None:
        assert v(u"123") == u"123"
    else:
        with pytest.raises(exc.PatternMatchError) as info:
            v(u"123")
        assert info.value.expected == pattern
        assert info.value.actual == u"123"


@pytest.mark.parametrize("class_", str_classes)
@pytest.mark.parametrize("options", [None, [u"abc", u"xyz"]])
def test_str_options(class_, options):
    # type: (t.Type[py.Str], t.Optional[t.Container[str]]) -> None
    v = class_(options=options)
    assert v(u"abc") == u"abc"
    assert v(u"xyz") == u"xyz"

    if options is None:
        assert v(u"123") == u"123"
    else:
        with pytest.raises(exc.OptionsError) as info:
            v(u"123")
        assert info.value.expected == options
        assert info.value.actual == u"123"


# =============================================================================


@pytest.mark.parametrize("class_", bytes_classes)
def test_bytes(class_):
    # type: (t.Type[py.Bytes]) -> None
    v = class_()
    assert v(b"abc") == b"abc"


@pytest.mark.parametrize("class_", bytes_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_bytes_nullable(class_, nullable):
    # type: (t.Type[py.Bytes], t.Optional[bool]) -> None
    v = class_(nullable=nullable)
    assert v(b"abc") == b"abc"

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == bytes
        assert info.value.actual == NoneType


@pytest.mark.parametrize("class_", bytes_classes)
@pytest.mark.parametrize("minlen", [None, 2])
@pytest.mark.parametrize("maxlen", [None, 5])
def test_bytes_minlen_maxlen(class_, minlen, maxlen):
    # type: (t.Type[py.Bytes], t.Optional[int], t.Optional[int]) -> None
    v = class_(minlen=minlen, maxlen=maxlen)
    assert v(b"abc") == b"abc"

    if minlen is None:
        assert v(b"a") == b"a"
    else:
        with pytest.raises(exc.MinLengthError) as info:
            v(b"a")
        assert info.value.expected == minlen
        assert info.value.actual == 1

    if maxlen is None:
        assert v(b"abcdef") == b"abcdef"
    else:
        with pytest.raises(exc.MaxLengthError) as info:
            v(b"abcdef")
        assert info.value.expected == maxlen
        assert info.value.actual == 6
