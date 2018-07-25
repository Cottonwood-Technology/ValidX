try:
    import typing as t  # noqa
except ImportError:
    pass

import pytest  # type: ignore

from validateit import py, cy
from validateit import exc


NoneType = type(None)
bool_classes = [py.Any, cy.Any]


@pytest.mark.parametrize("class_", bool_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_any(class_, nullable):
    # type: (t.Type[py.Any], t.Optional[bool]) -> None
    v = class_(nullable=nullable)
    assert v(True) is True
    assert v(1) == 1
    assert v("x") == "x"
    assert v([1, "x"]) == [1, "x"]

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected == object
        assert info.value.actual == NoneType
