from libc cimport limits

from copy import deepcopy

from .. import exc
from .. import contracts
from ..compat.colabc import Sequence, Mapping
from ..compat.types import chars
from . cimport abstract


cdef class List(abstract.Validator):
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

    cdef object _item
    cdef bint _nullable
    cdef long _minlen
    cdef long _maxlen
    cdef bint _unique

    @property
    def item(self):
        return self._item

    @property
    def nullable(self):
        return self._nullable

    @property
    def minlen(self):
        return None if self._minlen == 0 else self._minlen

    @property
    def maxlen(self):
        return None if self._maxlen == limits.LONG_MAX else self._maxlen

    @property
    def unique(self):
        return self._unique

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

        self._item = item
        self._nullable = nullable
        self._minlen = 0 if minlen is None else minlen
        self._maxlen = limits.LONG_MAX if maxlen is None else maxlen
        self._unique = unique

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

        cdef long length = len(result)
        if length < self._minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if length > self._maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)

        return result


cdef class Tuple(abstract.Validator):
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

    cdef tuple _items
    cdef bint _nullable

    @property
    def items(self):
        return self._items

    @property
    def nullable(self):
        return self._nullable

    def __init__(self, *items_, items=None, nullable=False, alias=None, replace=False):
        items = contracts.expect_sequence(
            self, "items", items or items_, item_type=abstract.Validator
        )
        nullable = contracts.expect_flag(self, "nullable", nullable)

        self._items = items
        self._nullable = nullable

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


cdef class Dict(abstract.Validator):
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

    cdef object _schema
    cdef bint _nullable
    cdef long _minlen
    cdef long _maxlen
    cdef tuple _extra
    cdef object _defaults
    cdef frozenset _optional
    cdef frozenset _dispose
    cdef frozenset _multikeys

    @property
    def schema(self):
        return self._schema

    @property
    def nullable(self):
        return self._nullable

    @property
    def minlen(self):
        return None if self._minlen == 0 else self._minlen

    @property
    def maxlen(self):
        return None if self._maxlen == limits.LONG_MAX else self._maxlen

    @property
    def extra(self):
        return self._extra

    @property
    def defaults(self):
        return self._defaults

    @property
    def optional(self):
        return self._optional

    @property
    def dispose(self):
        return self._dispose

    @property
    def multikeys(self):
        return self._multikeys

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

        self._schema = schema
        self._nullable = nullable
        self._minlen = 0 if minlen is None else minlen
        self._maxlen = limits.LONG_MAX if maxlen is None else maxlen
        self._extra = extra
        self._defaults = defaults
        self._optional = optional
        self._dispose = dispose
        self._multikeys = multikeys

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
                except exc.ValidationError as schema_error:
                    errors.extend(ne.add_context(key) for ne in schema_error)
            elif self.extra is not None:
                try:
                    key = self.extra[0](key, __context)
                except exc.ValidationError as extra_key_error:
                    errors.extend(
                        ne.add_context(exc.EXTRA_KEY).add_context(key)
                        for ne in extra_key_error
                    )
                try:
                    val = self.extra[1](val, __context)
                except exc.ValidationError as extra_value_error:
                    errors.extend(
                        ne.add_context(exc.EXTRA_VALUE).add_context(key)
                        for ne in extra_value_error
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
                        except exc.ValidationError as default_error:
                            errors.extend(ne.add_context(key) for ne in default_error)
                        continue
                if self.optional is not None and key in self.optional:
                    continue
                errors.append(exc.MissingKeyError(key))

        if errors:
            raise exc.SchemaError(errors)

        cdef long length = len(result)
        if length < self._minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if length > self._maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)

        return result
