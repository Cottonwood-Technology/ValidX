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
            "x": {"__class__": "Int", "min": 0, "max": 10},
            "y": {
                "__class__": "List",
                "item": {"__class__": "Int", "options": {1, 2, 3}},
                "nullable": True,
            },
        },
        "extra": [{"__class__": "Str"}, {"__class__": "Str"}],
    }
    v1 = module.Validator.load(data)
    assert isinstance(v1, module.Dict)
    assert isinstance(v1.schema["x"], module.Int)
    assert isinstance(v1.schema["y"], module.List)
    assert isinstance(v1.schema["y"].item, module.Int)
    assert isinstance(v1.extra, tuple)
    assert isinstance(v1.extra[0], module.Str)
    assert isinstance(v1.extra[1], module.Str)
    assert v1.schema["x"].min == 0
    assert v1.schema["x"].max == 10
    assert v1.schema["y"].nullable is True
    assert v1.schema["y"].item.options == frozenset([1, 2, 3])
    assert v1.dump() == data


def test_clone(module):
    v = module.Int()
    assert v.clone(nullable=True) == module.Int(nullable=True)

    v = module.Dict({"x": module.Int()})
    assert v.clone({"schema.x.nullable": True}) == (
        module.Dict({"x": module.Int(nullable=True)})
    )

    v = module.Int(min=0, max=100)
    assert v.clone({"-": ["min", "max"], "+": {"nullable": True}}) == (
        module.Int(nullable=True)
    )

    v = module.Int(options=[1, 2, 3])
    assert v.clone({"options+": [4, 5], "options-": [1, 2]}) == (
        module.Int(options=[3, 4, 5])
    )

    v = module.Dict({"x": module.Int(options=[1, 2, 3])})
    assert v.clone({"schema.x.options+": [4, 5], "schema.x.options-": [1, 2]}) == (
        module.Dict({"x": module.Int(options=[3, 4, 5])})
    )

    v = module.OneOf(module.Int(), module.Float())
    assert v.clone({"steps+": [module.Str()], "steps-": [module.Float()]}) == (
        module.OneOf(module.Int(), module.Str())
    )
    # fmt: off
    assert v.clone(
        {
            "steps+": [{"__class__": "Str"}],
            "steps-": [{"__class__": "Float"}],
        }
    ) == module.OneOf(module.Int(), module.Str())
    # fmt: on

    v = module.Dict({"x": module.Int()})
    with pytest.raises(KeyError) as info:
        v.clone({"schema-": ["y"]})
    assert info.value.args == ("'y' is not in dict at 'schema'",)

    v = module.Dict({"x": module.Int(options=[1, 2, 3])})
    with pytest.raises(KeyError) as info:
        v.clone({"schema.x.options-": [4]})
    assert info.value.args == ("4 is not in set at 'schema.x.options'",)

    v = module.Dict({"x": module.OneOf(module.Int(), module.Float())})
    with pytest.raises(ValueError) as info:
        v.clone({"schema.x.steps-": [module.Str()]})
    assert info.value.args == ("<Str()> is not in list at 'schema.x.steps'",)

    v = module.Dict({"x": module.Int()})
    with pytest.warns(DeprecationWarning) as record:
        assert v.clone(update={"/schema/x": {"nullable": True}}) == (
            module.Dict({"x": module.Int(nullable=True)})
        )
    assert len(record) == 1
    assert record[0].message.args[0] == (
        "This syntax is deprecated. Consider to use 'schema.x+' instead."
    )

    v = module.Dict({"x": module.Int(options=[1, 2, 3])})
    with pytest.warns(DeprecationWarning) as record:
        assert v.clone(unset={"/schema/x/options": [3]}) == (
            module.Dict({"x": module.Int(options=[1, 2])})
        )
    assert len(record) == 1
    assert record[0].message.args[0] == (
        "This syntax is deprecated. Consider to use 'schema.x.options-' instead "
        "and place it into update param."
    )


def test_alias(module):
    v1 = module.Int(alias="foo")
    assert module.instances.get("foo") is v1

    with pytest.raises(AssertionError):
        module.Str(alias="foo")

    v2 = module.Str(alias="foo", replace=True)
    assert module.instances.get("foo") is v2
    assert module.Validator.load({"__use__": "foo"}) is v2

    v3 = module.Validator.load({"__clone__": "foo", "update": {"nullable": True}})
    assert v3 is not v2
    assert isinstance(v3, module.Str)
    assert v3.nullable is True
