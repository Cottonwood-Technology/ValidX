import pytest

from validateit import py, cy


@pytest.fixture(params=[py, cy])
def module(request):
    yield request.param
    request.param.instances.clear()


def test_add_get(module):
    v = module.instances.add("foo", module.Int())
    assert isinstance(v, module.Int)
    assert v is module.instances.get("foo")

    with pytest.raises(AssertionError) as info:
        module.instances.add("foo", module.Str())
    assert info.value.args == ("Alias 'foo' of <Str()> conflicts with <Int()>",)

    v = module.instances.put("foo", module.Str())
    assert isinstance(v, module.Str)
    assert v is module.instances.get("foo")

    with pytest.raises(KeyError) as info:
        module.instances.get("unknown")
    assert info.value.args == ("Instance 'unknown' is not registered",)
