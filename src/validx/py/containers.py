from copy import deepcopy
from collections.abc import Sequence, Mapping

from .. import contracts
from .. import exc
from ..types import chars
from . import abstract


class List(abstract.Validator):
    """
    List Validator


    :param Validator item:
        validator for list items.

    :param bool nullable:
        accept ``None`` as a valid value.

    :param int minlen:
        lower length limit.

    :param int maxlen:
        upper length limit.

    :param bool unique:
        drop duplicate items.


    :raises InvalidTypeError:
        if ``not isinstance(value, (list, tuple))``.

    :raises MinLengthError:
        if ``len(value) < self.minlen``.

    :raises MaxLengthError:
        if ``len(value) > self.maxlen``.

    :raises SchemaError:
        with all errors,
        raised by item validator.

    """

    __slots__ = ("item", "nullable", "minlen", "maxlen", "unique")

    def __init__(
        self,
        item,
        nullable=False,
        minlen=None,
        maxlen=None,
        unique=False,
        alias=None,
        replace=False,
    ):
        item = contracts.expect(self, "item", item, types=abstract.Validator)
        nullable = contracts.expect_flag(self, "nullable", nullable)
        minlen = contracts.expect_length(self, "minlen", minlen, nullable=True)
        maxlen = contracts.expect_length(self, "maxlen", maxlen, nullable=True)
        unique = contracts.expect_flag(self, "unique", unique)

        setattr = object.__setattr__
        setattr(self, "item", item)
        setattr(self, "nullable", nullable)
        setattr(self, "minlen", minlen)
        setattr(self, "maxlen", maxlen)
        setattr(self, "unique", unique)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if __context is None:
            __context = {}  # Setup context, if it's top level call

        if value is None and self.nullable:
            return value
        if not isinstance(value, (list, tuple)):
            if not isinstance(value, Sequence) or isinstance(value, chars):
                raise exc.InvalidTypeError(expected=Sequence, actual=type(value))

        result = []
        errors = []
        if self.unique:
            unique = set()

        for num, val in enumerate(value):
            try:
                val = self.item(val, __context)
            except exc.ValidationError as e:
                errors.extend(ne.add_context(num) for ne in e)
                continue
            if self.unique:
                if val in unique:
                    continue
                unique.add(val)
            result.append(val)

        if errors:
            raise exc.SchemaError(errors)

        length = len(result)
        if self.minlen is not None and length < self.minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if self.maxlen is not None and length > self.maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)

        return result


class Tuple(abstract.Validator):
    """
    Tuple Validator


    :param Validator \\*items:
        validators for tuple members.

    :param bool nullable:
        accept ``None`` as a valid value.


    :raises InvalidTypeError:
        if ``not isinstance(value, (list, tuple))``.

    :raises TupleLengthError:
        if ``len(value) != len(self.items)``.

    :raises SchemaError:
        with all errors,
        raised by member validators.

    """

    __slots__ = ("items", "nullable")

    def __init__(self, *items_, items=None, nullable=False, alias=None, replace=False):
        items = contracts.expect_sequence(
            self, "items", items or items_, item_type=abstract.Validator
        )
        nullable = contracts.expect_flag(self, "nullable", nullable)

        setattr = object.__setattr__
        setattr(self, "items", items)
        setattr(self, "nullable", nullable)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if __context is None:
            __context = {}  # Setup context, if it's top level call

        if value is None and self.nullable:
            return value
        if not isinstance(value, (list, tuple)):
            if not isinstance(value, Sequence) or isinstance(value, chars):
                raise exc.InvalidTypeError(expected=Sequence, actual=type(value))
        if len(self.items) != len(value):
            raise exc.TupleLengthError(expected=len(self.items), actual=len(value))

        result = []
        errors = []

        for num, val in enumerate(value):
            try:
                val = self.items[num](val, __context)
            except exc.ValidationError as e:
                errors.extend(ne.add_context(num) for ne in e)
                continue
            result.append(val)

        if errors:
            raise exc.SchemaError(errors)
        return tuple(result)


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

    :param multikeys:
        list of keys that have to be treated as lists of values,
        if input value is a ``MultiDict`` (see notes below),
        i.e. value of these keys will be extracted using
        ``val = value.getall(key)`` or ``val = value.getlist(key)``.
    :type multikeys: list or tuple


    :raises InvalidTypeError:
        if ``not isinstance(value, collections.abc.Mapping)``.

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
        on error raised by ``extra`` validators,
        context marker :class:`validx.exc.Extra` will be used to indicate,
        which part of key/value pair is failed.


    It has been tested against the following implementations of ``MultiDict``:

    *   `WebOb MultiDict`_;
    *   `Werkzeug MultiDict`_;
    *   `MultiDict`_.

    However,
    it should work fine for other implementations,
    if the implementation is subclass of ``collections.abc.Mapping``,
    and provides ``getall()`` or ``getlist()`` methods.

    .. _WebOb MultiDict: https://docs.pylonsproject.org/projects/webob/en/stable/api/multidict.html#webob.multidict.MultiDict
    .. _Werkzeug MultiDict: http://werkzeug.pocoo.org/docs/0.14/datastructures/#werkzeug.datastructures.MultiDict
    .. _MultiDict: https://multidict.readthedocs.io/en/stable/

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

    def __init__(
        self,
        schema=None,
        nullable=False,
        minlen=None,
        maxlen=None,
        extra=None,
        defaults=None,
        optional=None,
        dispose=None,
        multikeys=None,
        alias=None,
        replace=False,
    ):
        schema = contracts.expect_mapping(
            self,
            "schema",
            schema,
            nullable=True,
            empty=True,
            value_type=abstract.Validator,
        )
        nullable = contracts.expect_flag(self, "nullable", nullable)
        minlen = contracts.expect_length(self, "minlen", minlen, nullable=True)
        maxlen = contracts.expect_length(self, "maxlen", maxlen, nullable=True)
        extra = contracts.expect_tuple(
            self,
            "extra",
            extra,
            nullable=True,
            struct=(abstract.Validator, abstract.Validator),
        )
        defaults = contracts.expect_mapping(
            self, "defaults", defaults, nullable=True, empty=True
        )
        optional = contracts.expect_container(
            self, "optional", optional, nullable=True, empty=True
        )
        dispose = contracts.expect_container(
            self, "dispose", dispose, nullable=True, empty=True
        )
        multikeys = contracts.expect_container(
            self, "multikeys", multikeys, nullable=True, empty=True
        )

        setattr = object.__setattr__
        setattr(self, "schema", schema)
        setattr(self, "nullable", nullable)
        setattr(self, "minlen", minlen)
        setattr(self, "maxlen", maxlen)
        setattr(self, "extra", extra)
        setattr(self, "defaults", defaults)
        setattr(self, "optional", optional)
        setattr(self, "dispose", dispose)
        setattr(self, "multikeys", multikeys)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if __context is None:
            __context = {}  # Setup context, if it's top level call

        if value is None and self.nullable:
            return value
        if not isinstance(value, (dict, Mapping)):
            raise exc.InvalidTypeError(expected=Mapping, actual=type(value))

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
            if getall is not None and key in self.multikeys:
                val = getall(key)
            if self.schema is not None and key in self.schema:
                try:
                    val = self.schema[key](val, __context)
                except exc.ValidationError as e:
                    errors.extend(ne.add_context(key) for ne in e)
            elif self.extra is not None:
                try:
                    key = self.extra[0](key, __context)
                except exc.ValidationError as e:
                    errors.extend(
                        ne.add_context(exc.EXTRA_KEY).add_context(key) for ne in e
                    )
                try:
                    val = self.extra[1](val, __context)
                except exc.ValidationError as e:
                    errors.extend(
                        ne.add_context(exc.EXTRA_VALUE).add_context(key) for ne in e
                    )
            else:
                errors.append(exc.ForbiddenKeyError(key))
            result[key] = val

        if self.schema is not None:
            for key, validator in self.schema.items():
                if key in result:
                    continue
                if self.defaults is not None:
                    try:
                        default = self.defaults[key]
                    except KeyError:
                        pass
                    else:
                        default = default() if callable(default) else deepcopy(default)
                        try:
                            result[key] = validator(default, __context)
                        except exc.ValidationError as e:
                            errors.extend(ne.add_context(key) for ne in e)
                        continue
                if self.optional is not None and key in self.optional:
                    continue
                errors.append(exc.MissingKeyError(key))

        if errors:
            raise exc.SchemaError(errors)

        length = len(result)
        if self.minlen is not None and length < self.minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if self.maxlen is not None and length > self.maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)

        return result
