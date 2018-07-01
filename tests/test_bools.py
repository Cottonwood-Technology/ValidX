try:
    import typing as t  # noqa
except ImportError:
    pass

import pytest  # type: ignore

from validateit import py, cy
from validateit import exc


NoneType = type(None)
bool_classes = [py.Bool, cy.Bool]


@pytest.mark.parametrize("class_", bool_classes)
def test_bool(class_):
    # type: (t.Type[py.Bool]) -> None
    v = class_()
    assert v(True) is True
    assert v(False) is False


@pytest.mark.parametrize("class_", bool_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_bool_nullable(class_, nullable):
    # type: (t.Type[py.Bool], t.Optional[bool]) -> None
    v = class_(nullable=nullable)
    assert v(True) is True
    assert v(False) is False

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == bool
        assert info.value.actual == NoneType


@pytest.mark.parametrize("class_", bool_classes)
@pytest.mark.parametrize("coerce_str", [None, False, True])
def test_bool_coerce_str(class_, coerce_str):
    # type: (t.Type[py.Bool], t.Optional[bool]) -> None
    v = class_(coerce_str=coerce_str)
    assert v(True) is True
    assert v(False) is False

    if coerce_str:
        assert v("0") is False
        assert v("False") is False
        assert v("false") is False
        assert v("No") is False
        assert v("no") is False
        assert v("Off") is False
        assert v("off") is False

        assert v("1") is True
        assert v("True") is True
        assert v("true") is True
        assert v("Yes") is True
        assert v("yes") is True
        assert v("On") is True
        assert v("on") is True

        with pytest.raises(exc.OptionsError) as info:
            v("abc")
        assert info.value.expected == class_.TRUE + class_.FALSE
        assert info.value.actual == "abc"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("0")
        assert info.value.expected == bool
        assert info.value.actual == str


@pytest.mark.parametrize("class_", bool_classes)
@pytest.mark.parametrize("coerce_int", [None, False, True])
def test_bool_coerce_int(class_, coerce_int):
    # type: (t.Type[py.Bool], t.Optional[bool]) -> None
    v = class_(coerce_int=coerce_int)
    assert v(True) is True
    assert v(False) is False

    if coerce_int:
        assert v(0) is False
        assert v(1) is True
        assert v(2) is True
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(0)
        assert info.value.expected == bool
        assert info.value.actual == int
