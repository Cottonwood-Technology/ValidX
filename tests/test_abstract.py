import pytest


def test_repr(module):
    v = module.Dict({"x": module.Int(min=0, max=100)}, nullable=True)
    assert repr(v) == (
        "<Dict(schema=frozendict({'x': <Int(min=0, max=100)>}), nullable=True)>"
    )

    v = module.Dict({"x": module.LazyRef("foo")})
    assert repr(v) == "<Dict(schema=frozendict({'x': <LazyRef(use='foo')>}))>"


def test_load_dump(module):
    data = {
        "__class__": "Dict",
        "schema": {
            u"x": {"__class__": "Int", "min": 0, "max": 10},
            u"y": {
                "__class__": "List",
                "item": {"__class__": "Int", "options": (1, 2, 3)},
                "nullable": True,
            },
        },
        "extra": ({"__class__": "Str"}, {"__class__": "Str"}),
    }
    v1 = module.Validator.load(data)
    assert isinstance(v1, module.Dict)
    assert isinstance(v1.schema[u"x"], module.Int)
    assert isinstance(v1.schema[u"y"], module.List)
    assert isinstance(v1.schema[u"y"].item, module.Int)
    assert isinstance(v1.extra, tuple)
    assert isinstance(v1.extra[0], module.Str)
    assert isinstance(v1.extra[1], module.Str)
    assert v1.schema[u"x"].min == 0
    assert v1.schema[u"x"].max == 10
    assert v1.schema[u"y"].nullable is True
    assert v1.schema[u"y"].item.options == (1, 2, 3)
    assert v1.dump() == data

    v2 = v1.clone(
        update={
            "/": {"optional": [u"x", u"y"]},
            "/schema/x": {"max": 100},
            "/schema/y/item/options": {2: 4, "extend": [5, 6]},
            "/extra/1": {"nullable": True},
        },
        unset={"/schema/x": ["min"], "/schema/y/item/options": [1]},
    )
    assert isinstance(v2, module.Dict)
    assert isinstance(v2.schema[u"x"], module.Int)
    assert isinstance(v2.schema[u"y"], module.List)
    assert isinstance(v2.schema[u"y"].item, module.Int)
    assert isinstance(v2.extra, tuple)
    assert isinstance(v2.extra[0], module.Str)
    assert isinstance(v2.extra[1], module.Str)
    assert v2.optional == [u"x", u"y"]
    assert v2.schema[u"x"].min is None
    assert v2.schema[u"x"].max == 100
    assert v2.schema[u"y"].nullable is True
    assert v2.schema[u"y"].item.options == (1, 4, 5, 6)
    assert v2.extra[1].nullable is True


def test_alias(module):
    v1 = module.Int(alias="foo")
    assert module.instances.get("foo") is v1

    with pytest.raises(AssertionError):
        module.Str(alias="foo")

    v2 = module.Str(alias="foo", replace=True)
    assert module.instances.get("foo") is v2
    assert module.Validator.load({"__use__": "foo"}) is v2

    v3 = module.Validator.load(
        {"__clone__": "foo", "update": {"/": {"nullable": True}}}
    )
    assert v3 is not v2
    assert isinstance(v3, module.Str)
    assert v3.nullable is True
