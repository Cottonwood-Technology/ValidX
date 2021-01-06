from validx.types import frozendict


def test_frozendict():
    d = frozendict({"x": 1})
    assert d["x"] == 1
    assert d.get("x") == 1
    assert d.get("y") is None
    assert "x" in d
    assert "y" not in d
    assert d == {"x": 1}
    assert repr(d) == "frozendict({'x': 1})"
    assert len(d) == 1
    assert list(iter(d)) == ["x"]
    assert list(d.items()) == [("x", 1)]
    assert list(d.keys()) == ["x"]
    assert list(d.values()) == [1]
