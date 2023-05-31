import pickle

import pytest

from validx import exc


NoneType = type(None)


def test_str(module):
    v = module.Str()
    assert v("abc") == "abc"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v


@pytest.mark.parametrize("nullable", [None, False, True])
def test_str_nullable(module, nullable):
    v = module.Str(nullable=nullable)
    assert v("abc") == "abc"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == str
        assert info.value.actual == NoneType


@pytest.mark.parametrize("coerce", [None, False, True])
@pytest.mark.parametrize("encoding", [None, "ascii"])
def test_str_coerce(module, coerce, encoding):
    v = module.Str(coerce=coerce, encoding=encoding)
    assert v("abc") == "abc"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if coerce:
        assert v(None) == "None"
        assert v(False) == "False"
        assert v(100) == "100"
        assert v(1.5) == "1.5"
        if encoding:
            assert v(b"abc") == "abc"
        else:
            assert v(b"abc") == "b'abc'"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(1.5)
        assert info.value.expected == str
        assert info.value.actual == float


@pytest.mark.parametrize("dontstrip", [None, False, True])
def test_dontstrip(module, dontstrip):
    v = module.Str(dontstrip=dontstrip)
    assert v("abc") == "abc"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if dontstrip:
        assert v(" \xa0\t\n\r\tabc\xa0\t\n\r\t ") == " \xa0\t\n\r\tabc\xa0\t\n\r\t "
    else:
        assert v(" \xa0\t\n\r\tabc\xa0\t\n\r\t ") == "abc"


@pytest.mark.parametrize("normspace", [None, False, True])
def test_normspace(module, normspace):
    v = module.Str(normspace=normspace)
    assert v("abc") == "abc"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if normspace:
        assert v("a  b\xa0\t\n\r\tc") == "a b c"
    else:
        assert v("a  b\xa0\t\n\r\tc") == "a  b\xa0\t\n\r\tc"


@pytest.mark.parametrize("encoding", [None, "utf-8"])
def test_str_encoding(module, encoding):
    v = module.Str(encoding=encoding)
    assert v("abc") == "abc"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if encoding:
        assert v(b"abc") == "abc"

        error = "café".encode("latin-1")
        with pytest.raises(exc.StrDecodeError) as info:
            v(error)
        assert info.value.expected == encoding
        assert info.value.actual == error
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(b"abc")
        assert info.value.expected == str
        assert info.value.actual == bytes


@pytest.mark.parametrize("minlen", [None, 2])
@pytest.mark.parametrize("maxlen", [None, 5])
def test_str_minlen_maxlen(module, minlen, maxlen):
    v = module.Str(minlen=minlen, maxlen=maxlen)
    assert v("abc") == "abc"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if minlen is None:
        assert v("a") == "a"
    else:
        with pytest.raises(exc.MinLengthError) as info:
            v("a")
        assert info.value.expected == minlen
        assert info.value.actual == 1

    if maxlen is None:
        assert v("abcdef") == "abcdef"
    else:
        with pytest.raises(exc.MaxLengthError) as info:
            v("abcdef")
        assert info.value.expected == maxlen
        assert info.value.actual == 6


@pytest.mark.parametrize("pattern", [None, "(?i)^[a-z]+$"])
def test_str_pattern(module, pattern):
    v = module.Str(pattern=pattern)
    assert v("abc") == "abc"
    assert v("ABC") == "ABC"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if pattern is None:
        assert v("123") == "123"
    else:
        with pytest.raises(exc.PatternMatchError) as info:
            v("123")
        assert info.value.expected == pattern
        assert info.value.actual == "123"


@pytest.mark.parametrize("options", [None, ["abc", "xyz"]])
def test_str_options(module, options):
    v = module.Str(options=options)
    assert v("abc") == "abc"
    assert v("xyz") == "xyz"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if options is None:
        assert v("123") == "123"
    else:
        with pytest.raises(exc.OptionsError) as info:
            v("123")
        assert info.value.expected == frozenset(options)
        assert info.value.actual == "123"


# =============================================================================


def test_bytes(module):
    v = module.Bytes()
    assert v(b"abc") == b"abc"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v


@pytest.mark.parametrize("nullable", [None, False, True])
def test_bytes_nullable(module, nullable):
    v = module.Bytes(nullable=nullable)
    assert v(b"abc") == b"abc"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == bytes
        assert info.value.actual == NoneType


@pytest.mark.parametrize("minlen", [None, 2])
@pytest.mark.parametrize("maxlen", [None, 5])
def test_bytes_minlen_maxlen(module, minlen, maxlen):
    v = module.Bytes(minlen=minlen, maxlen=maxlen)
    assert v(b"abc") == b"abc"
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

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
