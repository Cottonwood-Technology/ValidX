import pytest

from validateit import py, cy


@pytest.mark.parametrize("module", [py, cy])
def test_add_get(module):
    assert module.classes.get("Int") is module.Int

    with pytest.raises(AssertionError) as info:
        module.classes.add(module.Int)
    assert info.value.args == (
        "Name of %r conflicts with %r" % (module.Int, module.Int),
    )

    with pytest.raises(KeyError) as info:
        module.classes.get("Unknown")
    assert info.value.args == ("Class 'Unknown' is not registered",)
