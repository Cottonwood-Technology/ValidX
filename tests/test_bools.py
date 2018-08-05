import pytest

from validateit import exc


NoneType = type(None)


def test_bool(module):
    v = module.Bool()
    assert v(True) is True
    assert v(False) is False


@pytest.mark.parametrize("nullable", [None, False, True])
def test_bool_nullable(module, nullable):
    v = module.Bool(nullable=nullable)
    assert v(True) is True
    assert v(False) is False

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == bool
        assert info.value.actual == NoneType


@pytest.mark.parametrize("coerce_str", [None, False, True])
def test_bool_coerce_str(module, coerce_str):
    v = module.Bool(coerce_str=coerce_str)
    assert v(True) is True
    assert v(False) is False

    if coerce_str:
        assert v("0") is False
        assert v("False") is False
        assert v("false") is False
        assert v("No") is False
        assert v("no") is False
        assert v("n") is False
        assert v("Off") is False
        assert v("off") is False

        assert v("1") is True
        assert v("True") is True
        assert v("true") is True
        assert v("Yes") is True
        assert v("yes") is True
        assert v("y") is True
        assert v("On") is True
        assert v("on") is True

        with pytest.raises(exc.OptionsError) as info:
            v("abc")
        assert info.value.expected == module.Bool.TRUE + module.Bool.FALSE
        assert info.value.actual == "abc"
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v("0")
        assert info.value.expected == bool
        assert info.value.actual == str


@pytest.mark.parametrize("coerce_int", [None, False, True])
def test_bool_coerce_int(module, coerce_int):
    v = module.Bool(coerce_int=coerce_int)
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
