# coding: utf-8

from collections import deque
from textwrap import dedent

import pytest

from validateit import exc


def test_validation_error():
    te = exc.InvalidTypeError(expected=int, actual=str)
    assert te.context == deque([])
    assert te.format_context() == ""
    assert te.format_error() == "InvalidTypeError(expected=%r, actual=%r)" % (int, str)
    assert repr(te) == "<InvalidTypeError(expected=%r, actual=%r)>" % (int, str)
    te.add_context("x")
    assert te.context == deque(["x"])
    assert te.format_context() == "x"
    assert repr(te) == "<x: InvalidTypeError(expected=%r, actual=%r)>" % (int, str)
    te.add_context(1)
    assert te.context == deque([1, "x"])
    assert te.format_context() == "1.x"
    assert repr(te) == "<1.x: InvalidTypeError(expected=%r, actual=%r)>" % (int, str)
    te.add_context("a.b")
    assert te.format_context() == "[a.b].1.x"
    assert te.context == deque(["a.b", 1, "x"])
    assert repr(te) == "<[a.b].1.x: InvalidTypeError(expected=%r, actual=%r)>" % (
        int,
        str,
    )

    assert repr(te) == str(te)

    assert list(te) == [te]
    assert len(te) == 1
    assert te[0] == te
    with pytest.raises(IndexError):
        te[1]

    te.sort()
    assert list(te) == [te]
    te.sort(reverse=True)
    assert list(te) == [te]


def test_mapping_key_error():
    mke = exc.MissingKeyError("x")
    fke = exc.ForbiddenKeyError("y")
    assert mke.context == deque(["x"])
    assert fke.context == deque(["y"])
    assert repr(mke) == "<x: MissingKeyError()>"
    assert repr(fke) == "<y: ForbiddenKeyError()>"


def test_schema_error():
    mve_1 = exc.MaxValueError(context=deque(["y"]), expected=100, actual=200)
    mve_2 = exc.MaxValueError(context=deque(["x"]), expected=100, actual=300)

    se = exc.SchemaError(errors=[mve_1, mve_2])
    assert se.context == deque([])
    assert repr(se) == (
        dedent(
            """
            <SchemaError(errors=[
                <y: MaxValueError(expected=100, actual=200)>,
                <x: MaxValueError(expected=100, actual=300)>
            ])>
            """
        ).strip()
    )
    se.add_context("a")
    assert se.context == deque([])
    assert mve_1.context == deque(["a", "y"])
    assert mve_2.context == deque(["a", "x"])
    assert repr(se) == (
        dedent(
            """
            <SchemaError(errors=[
                <a.y: MaxValueError(expected=100, actual=200)>,
                <a.x: MaxValueError(expected=100, actual=300)>
            ])>
            """
        ).strip()
    )

    assert repr(se) == str(se)

    assert list(se) == [mve_1, mve_2]
    assert len(se) == 2
    assert se[0] == mve_1
    assert se[1] == mve_2
    with pytest.raises(IndexError):
        se[2]

    se.sort()
    assert list(se) == [mve_2, mve_1]
    se.sort(reverse=True)
    assert list(se) == [mve_1, mve_2]


def test_extra():
    assert exc.EXTRA_KEY == exc.Extra("KEY")
    assert exc.EXTRA_VALUE == exc.Extra("VALUE")
    assert exc.EXTRA_KEY != exc.EXTRA_VALUE
    assert repr(exc.EXTRA_KEY) == "@KEY"
    assert repr(exc.EXTRA_VALUE) == "@VALUE"
    assert str(exc.EXTRA_KEY) == repr(exc.EXTRA_KEY)


def test_step():
    step_1 = exc.Step(1)
    step_2 = exc.Step(2)
    assert step_1 != step_2
    assert step_1 == exc.Step(1)
    assert repr(step_1) == "#1"
    assert repr(step_2) == "#2"
    assert str(step_1) == repr(step_1)


def test_format_error():
    assert exc.format_error(exc.InvalidTypeError(expected=int, actual=type(None))) == [
        ("", u"Value should not be null.")
    ]
    assert exc.format_error(exc.InvalidTypeError(expected=int, actual=str)) == [
        ("", u"Expected type “int”, got “str”.")
    ]
    assert exc.format_error(exc.OptionsError(expected=[1], actual=2)) == [
        ("", u"Expected 1, got 2.")
    ]
    assert exc.format_error(exc.OptionsError(expected=[1, 2, 3], actual=4)) == [
        ("", u"Expected one of [1, 2, 3], got 4.")
    ]
    assert exc.format_error(exc.MinValueError(expected=10, actual=5)) == [
        ("", u"Expected value ≥ 10, got 5.")
    ]
    assert exc.format_error(exc.MaxValueError(expected=10, actual=15)) == [
        ("", u"Expected value ≤ 10, got 15.")
    ]
    assert exc.format_error(
        exc.FloatValueError(expected="finite", actual=float("-inf"))
    ) == [("", u"Expected finite number, got -∞.")]
    assert exc.format_error(
        exc.FloatValueError(expected="finite", actual=float("+inf"))
    ) == [("", u"Expected finite number, got +∞.")]
    assert exc.format_error(
        exc.FloatValueError(expected="number", actual=float("nan"))
    ) == [("", u"Expected number, got NaN.")]
    assert exc.format_error(exc.StrDecodeError(expected="utf-8", actual=b"\xFF")) == [
        ("", u"Cannot decode value using “utf-8” encoding.")
    ]
    assert exc.format_error(exc.MinLengthError(expected=10, actual=5)) == [
        ("", u"Expected value length ≥ 10, got 5.")
    ]
    assert exc.format_error(exc.MaxLengthError(expected=10, actual=15)) == [
        ("", u"Expected value length ≤ 10, got 15.")
    ]
    assert exc.format_error(exc.TupleLengthError(expected=1, actual=2)) == [
        ("", u"Expected exactly 1 element, got 2.")
    ]
    assert exc.format_error(exc.TupleLengthError(expected=3, actual=2)) == [
        ("", u"Expected exactly 3 elements, got 2.")
    ]
    assert exc.format_error(
        exc.PatternMatchError(expected="^[0-9]+$", actual="xyz")
    ) == [("", u"Cannot match “xyz” using “^[0-9]+$”.")]
    assert exc.format_error(
        exc.DatetimeParseError(expected="%Y-%m-%d", actual="08/18/2018")
    ) == [
        ("", u"Cannot parse date/time value from “08/18/2018” using “%Y-%m-%d” format.")
    ]
    assert exc.format_error(exc.RecursionMaxDepthError(expected=2, actual=3)) == [
        ("", u"Too many nested structures, limit is 2.")
    ]
    assert exc.format_error(exc.ForbiddenKeyError("x")) == [
        ("x", u"Key is not allowed.")
    ]
    assert exc.format_error(exc.MissingKeyError("x")) == [
        ("x", u"Required key is not provided.")
    ]

    # Test fallback
    assert exc.format_error(exc.ConditionError(expected=1, actual=2)) == [
        ("", "ConditionError(expected=1, actual=2)")
    ]
    assert exc.format_error(exc.FloatValueError(expected="something", actual=0.0)) == [
        ("", "FloatValueError(expected='something', actual=0.0)")
    ]
