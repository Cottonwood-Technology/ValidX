import collections as abc
from copy import deepcopy

try:
    import typing as t  # noqa
except ImportError:
    pass

from .. import exc
from . import abstract


class Dict(abstract.Validator):

    __slots__ = ("schema", "nullable", "extra", "defaults", "optional")

    def __init__(self, schema, **kw):
        super(Dict, self).__init__(schema=schema, **kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, dict):
            raise exc.InvalidTypeError(expected=dict, actual=type(value))

        result = {}  # type: t.Dict[t.Any, t.Any]
        errors = []  # type: t.List[t.Tuple[t.Any, exc.ValidationError]]

        for key, val in value.items():
            try:
                if key in self.schema:
                    val = self.schema[key](val)
                elif self.extra is not None:
                    key, val = self.extra((key, val))
                else:
                    errors.append((key, exc.ExtraKeyError(key=key)))
            except exc.ValidationError as e:
                errors.append((key, e))
                result[key] = None  # To prevent ``exc.RequiredKeyError`` below
                continue
            result[key] = val

        for key in self.schema:
            if key in result:
                continue
            if self.defaults is not None:
                try:
                    default = self.defaults[key]
                except KeyError:
                    pass
                else:
                    if callable(default):
                        result[key] = default()
                    else:
                        result[key] = deepcopy(default)
                    continue
            if self.optional is not None and key in self.optional:
                continue
            errors.append((key, exc.RequiredKeyError(key=key)))

        if errors:
            errors.sort(key=lambda item: item[0])
            raise exc.SchemaError(errors)
        return result


class Mapping(abstract.Validator):

    __slots__ = ("schema", "nullable", "extra", "defaults", "optional")

    def __init__(self, schema, **kw):
        super(Mapping, self).__init__(schema=schema, **kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, abc.Mapping):
            raise exc.InvalidTypeError(expected=abc.Mapping, actual=type(value))

        result = {}  # type: t.Dict[t.Any, t.Any]
        errors = []  # type: t.List[t.Tuple[t.Any, exc.ValidationError]]

        for key, val in value.items():
            try:
                if key in self.schema:
                    val = self.schema[key](val)
                elif self.extra is not None:
                    key, val = self.extra((key, val))
                else:
                    errors.append((key, exc.ExtraKeyError(key=key)))
            except exc.ValidationError as e:
                errors.append((key, e))
                result[key] = None  # To prevent ``exc.RequiredKeyError`` below
                continue
            result[key] = val

        for key in self.schema:
            if key in result:
                continue
            if self.defaults is not None:
                try:
                    default = self.defaults[key]
                except KeyError:
                    pass
                else:
                    if callable(default):
                        result[key] = default()
                    else:
                        result[key] = deepcopy(default)
                    continue
            if self.optional is not None and key in self.optional:
                continue
            errors.append((key, exc.RequiredKeyError(key=key)))

        if errors:
            errors.sort(key=lambda item: item[0])
            raise exc.SchemaError(errors)
        return result
