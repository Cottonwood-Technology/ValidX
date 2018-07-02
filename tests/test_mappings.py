import collections
import sys

try:
    import typing as t  # noqa
except ImportError:
    pass

import pytest  # type: ignore

from validateit import py, cy
from validateit import exc


if sys.version_info[0] < 3:
    str = unicode  # noqa


NoneType = type(None)
dict_classes = [py.Dict, py.Mapping, cy.Dict, cy.Mapping]


class CustomMapping(collections.Mapping):
    def __init__(self, content):
        self.content = content

    def __getitem__(self, key):
        return self.content[key]

    def __iter__(self):
        return iter(self.content)

    def __len__(self):
        return len(self.content)


@pytest.mark.parametrize("class_", dict_classes)
def test_dict(class_):
    # type: (t.Type[py.Dict]) -> None
    v = class_({u"x": py.Int(), u"y": py.Int()})
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}
    assert v(collections.OrderedDict({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    assert v(collections.defaultdict(None, {u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}

    if class_.__name__ == "Mapping":
        assert v(CustomMapping({u"x": 1, u"y": 2})) == {u"x": 1, u"y": 2}
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(CustomMapping({u"x": 1, u"y": 2}))
        assert info.value.expected == dict
        assert info.value.actual == CustomMapping

    with pytest.raises(exc.InvalidTypeError) as info:
        v([(u"x", 1), (u"y", 2)])
    assert info.value.expected in (dict, collections.Mapping)
    assert info.value.actual == list

    with pytest.raises(exc.SchemaError) as info:
        v({u"x": u"1", u"y": None})
    assert len(info.value.errors) == 2

    ne_1, ne_2 = info.value.errors

    assert isinstance(ne_1, exc.InvalidTypeError)
    assert ne_1.context == [u"x"]
    assert ne_1.expected == int
    assert ne_1.actual == str

    assert isinstance(ne_2, exc.InvalidTypeError)
    assert ne_2.context == [u"y"]
    assert ne_2.expected == int
    assert ne_2.actual == NoneType


@pytest.mark.parametrize("class_", dict_classes)
@pytest.mark.parametrize("nullable", [None, False, True])
def test_dict_nullable(class_, nullable):
    # type: (t.Type[py.Dict], t.Optional[bool]) -> None
    v = class_({u"x": py.Int(), u"y": py.Int()}, nullable=nullable)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}

    if nullable:
        assert v(None) is None
    else:
        with pytest.raises(exc.InvalidTypeError) as info:
            v(None)
        assert info.value.expected in (dict, collections.Mapping)
        assert info.value.actual == NoneType


@pytest.mark.parametrize("class_", dict_classes)
@pytest.mark.parametrize("defaults", [None, {u"x": 0}, {u"x": lambda: 0}])
@pytest.mark.parametrize("optional", [None, [u"x"]])
def test_dict_defaults_and_optional(class_, defaults, optional):
    # type: (t.Type[py.Dict], t.Optional[t.Dict], t.Optional[t.List]) -> None
    v = class_({u"x": py.Int(), u"y": py.Int()}, defaults=defaults, optional=optional)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}

    with pytest.raises(exc.SchemaError) as info:
        v({u"x": 1})
    assert len(info.value.errors) == 1
    ne = info.value.errors[0]
    assert isinstance(ne, exc.MissingKeyError)
    assert ne.context == [u"y"]

    if defaults:
        assert v({u"y": 2}) == {u"x": 0, u"y": 2}
    elif optional:
        assert v({u"y": 2}) == {u"y": 2}
    else:
        with pytest.raises(exc.SchemaError) as info:
            v({u"y": 2})
        assert len(info.value.errors) == 1
        ne = info.value.errors[0]
        assert isinstance(ne, exc.MissingKeyError)
        assert ne.context == [u"x"]


@pytest.mark.parametrize("class_", dict_classes)
@pytest.mark.parametrize("extra", [None, (py.Str(), py.Int())])
def test_dict_extra(class_, extra):
    # type: (t.Type[py.Dict], t.Optional[t.Tuple[py.Str, py.Int]]) -> None
    v = class_({u"x": py.Int(), u"y": py.Int()}, extra=extra)
    assert v({u"x": 1, u"y": 2}) == {u"x": 1, u"y": 2}

    if extra:
        assert v({u"x": 1, u"y": 2, u"z": 3}) == {u"x": 1, u"y": 2, u"z": 3}

        with pytest.raises(exc.SchemaError) as info:
            v({u"x": 1, u"y": 2, 3: None})
        assert len(info.value.errors) == 1

        ne = info.value.errors[0]

        assert isinstance(ne, exc.ExtraKeyError)
        assert ne.context == [3]

        assert isinstance(ne.key_error, exc.InvalidTypeError)
        assert ne.key_error.expected == str
        assert ne.key_error.actual == int

        assert isinstance(ne.value_error, exc.InvalidTypeError)
        assert ne.value_error.expected == int
        assert ne.value_error.actual == NoneType
    else:
        with pytest.raises(exc.SchemaError) as info:
            v({u"x": 1, u"y": 2, u"z": 3})
        assert len(info.value.errors) == 1
        ne = info.value.errors[0]
        assert isinstance(ne, exc.ForbiddenKeyError)
        assert ne.context == [u"z"]
