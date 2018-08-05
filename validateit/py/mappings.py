import collections as abc
from copy import deepcopy

try:
    import typing as t  # noqa
except ImportError:  # pragma: no cover
    pass

from .. import exc
from . import abstract


class Dict(abstract.Validator):
    """
    Dictionary Validator


    :param dict schema:
        schema validator in format ``{<key>: <validator>}``.

    :param bool nullable:
        accept ``None`` as a valid value.

    :param int minlen:
        lower length limit.

    :param int maxlen:
        upper length limit.

    :param tuple extra:
        validators for extra keys and values in format
        ``(<key_validator>, <value_validator>)``,
        it is used for keys are not presented in ``schema``.

    :param dict defaults:
        default values for missing keys.

    :param optional:
        list of optional keys.
    :type optional: list or tuple

    :param dispose:
        list of keys that have to be silently removed.
    :type dispose: list or tuple


    :raises InvalidTypeError:
        if ``not isinstance(value, dict)``.

    :raises MinLengthError:
        if ``len(value) < self.minlen``.

    :raises MaxLengthError:
        if ``len(value) > self.maxlen``.

    :raises SchemaError:
        with all errors,
        raised by schema validators,
        extra validators,
        and missing required and forbidden extra keys.


    :note:
        Dictionary validator is a twin of :class:`Mapping`,
        but it accepts only ``dict`` as a valid input value.
        Because of this,
        it is **less flexible**,
        but works **faster** than :class:`Mapping`.

    """

    __slots__ = (
        "schema",
        "nullable",
        "minlen",
        "maxlen",
        "extra",
        "defaults",
        "optional",
        "dispose",
    )

    def __init__(self, schema=None, **kw):
        super(Dict, self).__init__(schema=schema, **kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, dict):
            raise exc.InvalidTypeError(expected=dict, actual=type(value))

        length = len(value)
        if self.minlen is not None and length < self.minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if self.maxlen is not None and length > self.maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)

        result = {}
        errors = []

        for key, val in value.items():
            if self.dispose is not None and key in self.dispose:
                continue
            try:
                if self.schema is not None and key in self.schema:
                    val = self.schema[key](val)
                elif self.extra is not None:
                    try:
                        key = self.extra[0](key)
                    except exc.ValidationError as e:
                        extra_key_error = e
                    else:
                        extra_key_error = None
                    try:
                        val = self.extra[1](val)
                    except exc.ValidationError as e:
                        extra_value_error = e
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

        if self.schema is not None:
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
    """
    Arbitrary Mapping Validator


    :param dict schema:
        schema validator in format ``{<key>: <validator>}``.

    :param bool nullable:
        accept ``None`` as a valid value.

    :param int minlen:
        lower length limit.

    :param int maxlen:
        upper length limit.

    :param tuple extra:
        validators for extra keys and values in format
        ``(<key_validator>, <value_validator>)``,
        it is used for keys are not presented in ``schema``.

    :param dict defaults:
        default values for missing keys.

    :param optional:
        list of optional keys.
    :type optional: list or tuple

    :param dispose:
        list of keys that have to be silently removed.
    :type dispose: list or tuple

    :param multikeys:
        list of keys that have to be treated as lists of values,
        if input value is a ``MultiDict`` (see notes below),
        i.e. value of these keys will be extracted using
        ``val = value.getall(key)`` or ``val = value.getlist(key)``.
    :type multikeys: list or tuple


    :raises InvalidTypeError:
        if ``not isinstance(value, collections.Mapping)``.

    :raises MinLengthError:
        if ``len(value) < self.minlen``.

    :raises MaxLengthError:
        if ``len(value) > self.maxlen``.

    :raises SchemaError:
        with all errors,
        raised by schema validators,
        extra validators,
        and missing required and forbidden extra keys.


    :note:
        Mapping validator is a twin of :class:`Dict`,
        but it accepts arbitrary mapping type as a valid input value.
        Because of this,
        it is **more flexible**,
        but works **slower** than :class:`Dict`.

    :note: TODO: MultiDict notes

    """

    __slots__ = (
        "schema",
        "nullable",
        "minlen",
        "maxlen",
        "extra",
        "defaults",
        "optional",
        "dispose",
        "multikeys",
    )

    def __init__(self, schema=None, **kw):
        super(Mapping, self).__init__(schema=schema, **kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, abc.Mapping):
            raise exc.InvalidTypeError(expected=abc.Mapping, actual=type(value))

        length = len(value)
        if self.minlen is not None and length < self.minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if self.maxlen is not None and length > self.maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)

        result = {}
        errors = []
        getall = None
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
                if self.schema is not None and key in self.schema:
                    val = self.schema[key](val)
                elif self.extra is not None:
                    try:
                        key = self.extra[0](key)
                    except exc.ValidationError as e:
                        extra_key_error = e
                    else:
                        extra_key_error = None
                    try:
                        val = self.extra[1](val)
                    except exc.ValidationError as e:
                        extra_value_error = e
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

        if self.schema is not None:
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
