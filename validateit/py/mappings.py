import collections as abc
from copy import deepcopy

try:
    import typing as t  # noqa
except ImportError:  # pragma: no cover
    pass

from .. import exc
from . import abstract


class Dict(abstract.Validator):

    __slots__ = ("schema", "nullable", "extra", "defaults", "optional", "dispose")

    def __init__(self, schema, **kw):
        super(Dict, self).__init__(schema=schema, **kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, dict):
            raise exc.InvalidTypeError(expected=dict, actual=type(value))

        result = {}  # type: t.Dict[t.Any, t.Any]
        errors = []  # type: t.List[exc.ValidationError]

        for key, val in value.items():
            if self.dispose is not None and key in self.dispose:
                continue
            try:
                if key in self.schema:
                    val = self.schema[key](val)
                elif self.extra is not None:
                    try:
                        key = self.extra[0](key)
                    except exc.ValidationError as e:
                        extra_key_error = e  # type: t.Optional[exc.ValidationError]
                    else:
                        extra_key_error = None
                    try:
                        val = self.extra[1](val)
                    except exc.ValidationError as e:
                        extra_value_error = e  # type: t.Optional[exc.ValidationError]
                    else:
                        extra_value_error = None
                    if extra_key_error is not None or extra_value_error is not None:
                        errors.append(
                            exc.ExtraKeyError(
                                key,
                                key_error=extra_key_error,
                                value_error=extra_value_error,
                            )
                        )
                else:
                    errors.append(exc.ForbiddenKeyError(key))
            except exc.ValidationError as e:
                errors.extend(ne.add_context(key) for ne in e)
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
            errors.append(exc.MissingKeyError(key))

        if errors:
            errors.sort(key=lambda e: e.context)
            raise exc.SchemaError(errors)
        return result


class Mapping(abstract.Validator):

    __slots__ = (
        "schema",
        "nullable",
        "extra",
        "defaults",
        "optional",
        "dispose",
        "multikeys",
    )

    def __init__(self, schema, **kw):
        super(Mapping, self).__init__(schema=schema, **kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, abc.Mapping):
            raise exc.InvalidTypeError(expected=abc.Mapping, actual=type(value))

        result = {}  # type: t.Dict[t.Any, t.Any]
        errors = []  # type: t.List[exc.ValidationError]
        getall = None  # type: t.Optional[t.Callable[[t.Any], t.List]]
        if self.multikeys is not None:
            # If value is a multidict, specified keys should be treated
            # as sequences, not as scalars.  The following popular multidict
            # interfaces are supported:
            #   multidict (value.getall)
            #   webob.multidict (value.getall)
            #   werkzeug.datastructures.MultiDict (value.getlist)
            getall = getattr(value, "getall", None) or getattr(value, "getlist", None)

        for key, val in value.items():
            if self.dispose is not None and key in self.dispose:
                continue
            if (
                self.multikeys is not None
                and getall is not None
                and key in self.multikeys
            ):
                val = getall(key)
            try:
                if key in self.schema:
                    val = self.schema[key](val)
                elif self.extra is not None:
                    try:
                        key = self.extra[0](key)
                    except exc.ValidationError as e:
                        extra_key_error = e  # type: t.Optional[exc.ValidationError]
                    else:
                        extra_key_error = None
                    try:
                        val = self.extra[1](val)
                    except exc.ValidationError as e:
                        extra_value_error = e  # type: t.Optional[exc.ValidationError]
                    else:
                        extra_value_error = None
                    if extra_key_error is not None or extra_value_error is not None:
                        errors.append(
                            exc.ExtraKeyError(
                                key,
                                key_error=extra_key_error,
                                value_error=extra_value_error,
                            )
                        )
                else:
                    errors.append(exc.ForbiddenKeyError(key))
            except exc.ValidationError as e:
                errors.extend(ne.add_context(key) for ne in e)
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
            errors.append(exc.MissingKeyError(key))

        if errors:
            errors.sort(key=lambda e: e.context)
            raise exc.SchemaError(errors)
        return result
