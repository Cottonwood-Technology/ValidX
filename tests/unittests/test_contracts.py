from functools import partial
from collections.abc import Sequence, Container, Mapping, Callable

import pytest

from validx import contracts
from validx.types import numbers, chars, frozendict


class ContextMock(object):
    pass


obj = ContextMock()


def test_expect():
    c = partial(contracts.expect, obj, "attr", types=numbers, convert_to=float)
    assert c(1) == 1.0
    assert c(1.0) == 1.0
    assert c(None, nullable=True) is None

    with pytest.raises(TypeError) as info:
        c(None)
    assert info.value.args == (
        (
            "%s.ContextMock.attr should be of type %r"
            % (ContextMock.__module__, numbers)
        ),
    )

    c = partial(contracts.expect, obj, "attr", types=Sequence)
    assert c([1, 2, 3]) == [1, 2, 3]
    assert c("abc") == "abc"

    with pytest.raises(TypeError) as info:
        c("abc", not_types=chars)
    assert info.value.args == (
        (
            "%s.ContextMock.attr should not be of type %r"
            % (ContextMock.__module__, chars)
        ),
    )


def test_expect_flag():
    c = partial(contracts.expect_flag, obj, "attr")
    assert c(None) is False
    assert c(0) is False
    assert c(1) is True
    assert c(True) is True
    assert c(False) is False

    with pytest.raises(TypeError) as info:
        c("true")
    assert info.value.args == (
        (
            "%s.ContextMock.attr should be of type %r"
            % (ContextMock.__module__, (bool, int, type(None)))
        ),
    )


def test_expect_length():
    c = partial(contracts.expect_length, obj, "attr")
    assert c(0) == 0
    assert c(1) == 1
    assert c(10) == 10
    assert c(None, nullable=True) is None

    with pytest.raises(TypeError) as info:
        c(None)
    assert info.value.args == (
        ("%s.ContextMock.attr should be of type %r" % (ContextMock.__module__, int)),
    )
    with pytest.raises(TypeError) as info:
        c(1.0)
    assert info.value.args == (
        ("%s.ContextMock.attr should be of type %r" % (ContextMock.__module__, int)),
    )
    with pytest.raises(ValueError) as info:
        c(-1)
    assert info.value.args == (
        ("%s.ContextMock.attr should not be negative number" % ContextMock.__module__),
    )


def test_expect_str():
    c = partial(contracts.expect_str, obj, "attr")
    assert c("abc") == "abc"
    assert c(None, nullable=True) is None

    with pytest.raises(TypeError) as info:
        c(None)
    assert info.value.args == (
        ("%s.ContextMock.attr should be of type %r" % (ContextMock.__module__, str)),
    )


def test_expect_callable():
    def somefunc():
        pass

    c = partial(contracts.expect_callable, obj, "attr")
    assert c(somefunc) is somefunc
    assert c(None, nullable=True) is None

    with pytest.raises(TypeError) as info:
        c(None)
    assert info.value.args == (
        (
            "%s.ContextMock.attr should be of type %r"
            % (ContextMock.__module__, Callable)
        ),
    )


def test_expect_container():
    c = partial(contracts.expect_container, obj, "attr")
    assert c([1, 2, 3]) == frozenset([1, 2, 3])
    assert c([{}, {}]) == ({}, {})
    assert c(None, nullable=True) is None
    assert c([], empty=True) == frozenset([])
    assert c([1, "x"]) == frozenset([1, "x"])

    with pytest.raises(TypeError) as info:
        c("abc")
    assert info.value.args == (
        (
            "%s.ContextMock.attr should not be of type %r"
            % (ContextMock.__module__, chars)
        ),
    )
    with pytest.raises(TypeError) as info:
        c(None)
    assert info.value.args == (
        (
            "%s.ContextMock.attr should be of type %r"
            % (ContextMock.__module__, Container)
        ),
    )
    with pytest.raises(ValueError) as info:
        c([])
    assert info.value.args == (
        ("%s.ContextMock.attr should not be empty" % (ContextMock.__module__)),
    )
    with pytest.raises(TypeError) as info:
        c([1, "x"], item_type=int)
    assert info.value.args == (
        (
            "%s.ContextMock.attr items should be of type %r, got %r"
            % (ContextMock.__module__, int, str)
        ),
    )


def test_expect_sequence():
    c = partial(contracts.expect_sequence, obj, "attr")
    assert c([1, 2, 3]) == (1, 2, 3)
    assert c([{}, {}]) == ({}, {})
    assert c(None, nullable=True) is None
    assert c([], empty=True) == ()
    assert c([1, "x"]) == (1, "x")

    with pytest.raises(TypeError) as info:
        c("abc")
    assert info.value.args == (
        (
            "%s.ContextMock.attr should not be of type %r"
            % (ContextMock.__module__, chars)
        ),
    )
    with pytest.raises(TypeError) as info:
        c(None)
    assert info.value.args == (
        (
            "%s.ContextMock.attr should be of type %r"
            % (ContextMock.__module__, Sequence)
        ),
    )
    with pytest.raises(ValueError) as info:
        c([])
    assert info.value.args == (
        ("%s.ContextMock.attr should not be empty" % (ContextMock.__module__)),
    )
    with pytest.raises(TypeError) as info:
        c([1, "x"], item_type=int)
    assert info.value.args == (
        (
            "%s.ContextMock.attr[1] value should be of type %r"
            % (ContextMock.__module__, int)
        ),
    )


def test_expect_mapping():
    c = partial(contracts.expect_mapping, obj, "attr")
    assert c({"a": 1, "b": 2}) == frozendict({"a": 1, "b": 2})
    assert c({}, empty=True) == frozendict({})
    assert c(None, nullable=True) is None
    assert c({"a": 1, "b": "x"}) == frozendict({"a": 1, "b": "x"})

    with pytest.raises(TypeError) as info:
        c(None)
    assert info.value.args == (
        (
            "%s.ContextMock.attr should be of type %r"
            % (ContextMock.__module__, Mapping)
        ),
    )
    with pytest.raises(ValueError) as info:
        c({})
    assert info.value.args == (
        ("%s.ContextMock.attr should not be empty" % (ContextMock.__module__)),
    )
    with pytest.raises(TypeError) as info:
        c({"a": 1, "b": "x"}, value_type=int)
    assert info.value.args == (
        (
            "%s.ContextMock.attr['b'] value should be of type %r"
            % (ContextMock.__module__, int)
        ),
    )


def test_expect_tuple():
    c = partial(contracts.expect_tuple, obj, "attr", struct=(int, str))
    assert c([1, "x"]) == (1, "x")
    assert c(None, nullable=True) is None

    with pytest.raises(TypeError) as info:
        c("abc")
    assert info.value.args == (
        (
            "%s.ContextMock.attr should not be of type %r"
            % (ContextMock.__module__, chars)
        ),
    )
    with pytest.raises(TypeError) as info:
        c(None)
    assert info.value.args == (
        (
            "%s.ContextMock.attr should be of type %r"
            % (ContextMock.__module__, Sequence)
        ),
    )
    with pytest.raises(ValueError) as info:
        c([1, 2, 3])
    assert info.value.args == (
        (
            "%s.ContextMock.attr should be a tuple of %r"
            % (ContextMock.__module__, (int, str))
        ),
    )
    with pytest.raises(TypeError) as info:
        c([1, 2])
    assert info.value.args == (
        (
            "%s.ContextMock.attr[1] value should be of type %r"
            % (ContextMock.__module__, str)
        ),
    )
