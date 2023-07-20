import pickle
from collections import deque

import pytest

from validx import exc


NoneType = type(None)


def test_lazyref(module):
    v = module.Dict(
        {"x": module.Int(), "y": module.LazyRef("foo", maxdepth=2)},
        alias="foo",
        optional=["x", "y"],
    )

    data = {"x": 1}
    assert v(data) == data

    data = {"y": {"x": 1}}
    assert v(data) == data

    data = {"y": {"y": {"x": 1}}}
    assert v(data) == data

    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    with pytest.raises(exc.SchemaError) as info:
        v({"y": {"y": {"y": {"x": 1}}}})
    assert len(info.value) == 1

    assert isinstance(info.value[0], exc.RecursionMaxDepthError)
    assert info.value[0].context == deque(["y", "y", "y"])
    assert info.value[0].expected == 2
    assert info.value[0].actual == 3


def test_lazyref_context(module):
    class MarkContext(module.Validator):
        def __call__(self, value, __context=None):
            __context["marked"] = True
            return value

    MarkContext(alias="foo")
    v = module.LazyRef("foo")

    context = {}
    v(None, context)
    assert context["marked"]

    v = module.LazyRef("foo", maxdepth=1)

    context = {}
    v(None, context)
    assert context["marked"]
    assert context["foo.recursion_depth"] == 0


# =============================================================================


def test_type(module):
    v = module.Type(int)
    assert v(5) == 5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    with pytest.raises(exc.InvalidTypeError) as info:
        v(5.0)
    assert info.value.expected == int
    assert info.value.actual == float


def test_type_metaclass(module):
    class MetaClass(type):
        pass

    CustomType = MetaClass("CustomType", (), {})

    v = module.Type(CustomType)
    obj = CustomType()
    assert v(obj) is obj


@pytest.mark.parametrize("nullable", [None, False, True])
def test_type_nullable(module, nullable):
    v = module.Type(int, nullable=nullable)
    assert v(5) == 5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == int
        assert info.value.actual == NoneType


@pytest.mark.parametrize("nullable", [None, False, True])
def test_type_object_nullable(module, nullable):
    v = module.Type(object, nullable=nullable)
    assert v(5) == 5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == object
        assert info.value.actual == NoneType


@pytest.mark.parametrize("coerce", [None, False, True])
def test_type_coerce(module, coerce):
    v = module.Type(int, coerce=coerce)
    assert v(5) == 5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if coerce:
        assert v(5.5) == 5
        assert v("5") == 5

        with pytest.raises(exc.CoerceError) as info:
            v("abc")
        assert info.value.expected == int
        assert info.value.actual == "abc"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(5.5)
        assert info.value.expected == int
        assert info.value.actual == float

        with pytest.raises(exc.InvalidTypeError) as info:
            v("5")
        assert info.value.expected == int
        assert info.value.actual == str


@pytest.mark.parametrize("min", [None, 0])
@pytest.mark.parametrize("max", [None, 10])
def test_type_min_max(module, min, max):
    v = module.Type(int, min=min, max=max)
    assert v(5) == 5
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if min is None:
        assert v(-1) == -1
    else:
        with pytest.raises(exc.MinValueError) as info:
            v(-1)
        assert info.value.expected == min
        assert info.value.actual == -1

    if max is None:
        assert v(11) == 11
    else:
        with pytest.raises(exc.MaxValueError) as info:
            v(11)
        assert info.value.expected == max
        assert info.value.actual == 11


@pytest.mark.parametrize("minlen", [None, 2])
@pytest.mark.parametrize("maxlen", [None, 5])
def test_type_minlen_maxlen(module, minlen, maxlen):
    if minlen or maxlen:
        with pytest.raises(TypeError) as info:
            module.Type(int, minlen=minlen, maxlen=maxlen)
        assert info.value.args[0] == "Type %r does not provide method '__len__()'" % int

    v = module.Type(bytes, minlen=minlen, maxlen=maxlen)
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


@pytest.mark.parametrize("options", [None, [5, 6]])
def test_type_options(module, options):
    v = module.Type(int, options=options)
    assert v(5) == 5
    assert v(6) == 6
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    if options is None:
        assert v(4) == 4
    else:
        with pytest.raises(exc.OptionsError) as info:
            v(4)
        assert info.value.expected == frozenset(options)
        assert info.value.actual == 4


# =============================================================================


def test_const(module):
    v = module.Const(1)
    assert v(1) == 1
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v

    with pytest.raises(exc.OptionsError) as info:
        v(2)
    assert info.value.expected == [1]
    assert info.value.actual == 2


@pytest.mark.parametrize("value", [False, None])
def test_const_false_and_none(module, value):
    v = module.Const(value)
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v
    assert repr(v) == f"<Const(value={value!r})>"


# =============================================================================


def test_any(module):
    v = module.Any()
    assert v(None) is None
    assert v(True) is True
    assert v(1) == 1
    assert v("x") == "x"
    assert v([1, "x"]) == [1, "x"]
    assert v.clone() == v
    assert pickle.loads(pickle.dumps(v)) == v
