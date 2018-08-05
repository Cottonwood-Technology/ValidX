from collections import deque
from textwrap import dedent

from validateit import exc


def test_exc():
    te = exc.InvalidTypeError(expected=int, actual=str)
    assert te.context == deque([])
    assert repr(te) == "<InvalidTypeError(expected=%r, actual=%r)>" % (int, str)
    te.add_context("x")
    assert te.context == deque(["x"])
    assert repr(te) == "<x: InvalidTypeError(expected=%r, actual=%r)>" % (int, str)
    te.add_context(1)
    assert te.context == deque([1, "x"])
    assert repr(te) == "<1.x: InvalidTypeError(expected=%r, actual=%r)>" % (int, str)
    te.add_context("a.b")
    assert te.context == deque(["a.b", 1, "x"])
    assert repr(te) == "<[a.b].1.x: InvalidTypeError(expected=%r, actual=%r)>" % (
        int,
        str,
    )
    assert repr(te) == str(te)

    me = exc.MissingKeyError("x")
    assert me.context == deque(["x"])
    assert repr(me) == "<x: MissingKeyError()>"
    assert repr(me) == str(me)

    se = exc.SchemaError(errors=[te, me])
    assert se.context == deque([])
    assert repr(se) == (
        dedent(
            """
            <SchemaError(errors=[
                %r,
                %r
            ])>
            """
        ).strip()
        % (te, me)
    )
    se.add_context("y")
    assert se.context == deque([])
    assert te.context == deque(["y", "a.b", 1, "x"])
    assert me.context == deque(["y", "x"])
    assert repr(se) == str(se)

    assert list(te) == [te]
    assert list(me) == [me]
    assert list(se) == [te, me]


def test_step():
    step_1 = exc.Step(1)
    step_2 = exc.Step(2)
    assert step_1 != step_2
    assert step_1 == exc.Step(1)
    assert repr(step_1) == "#1"
    assert repr(step_2) == "#2"
    assert str(step_1) == repr(step_1)
