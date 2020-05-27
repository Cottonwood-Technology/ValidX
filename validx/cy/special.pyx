from libc cimport limits

from .. import exc
from .. import contracts
from . cimport abstract, instances


cdef class LazyRef(abstract.Validator):
    """
    Lazy Referenced Validator

    It is useful to build validators for recursive structures.

    ..  testsetup:: lazyref

        from validx import Dict, Int, LazyRef, instances

    ..  testcleanup:: lazyref

        instances.clear()

    ..  doctest:: lazyref
        :options: +ELLIPSIS, -IGNORE_EXCEPTION_DETAIL

        >>> schema = Dict(
        ...     {
        ...         "foo": Int(),
        ...         "bar": LazyRef("schema", maxdepth=1),
        ...     },
        ...     optional=("foo", "bar"),
        ...     minlen=1,
        ...     alias="schema",
        ... )

        >>> schema({"foo": 1})
        {'foo': 1}

        >>> schema({"bar": {"foo": 1}})
        {'bar': {'foo': 1}}

        >>> schema({"bar": {"bar": {"foo": 1}}})
        Traceback (most recent call last):
            ...
        validx.exc.errors.SchemaError: <SchemaError(errors=[
            <bar.bar: RecursionMaxDepthError(expected=1, actual=2)>
        ])>

    :param str use:
        alias of referenced validator.

    :param int maxdepth:
        maximum recursion depth.


    :raises RecursionMaxDepthError:
        if ``self.maxdepth is not None``
        and current recursion depth exceeds the limit.

    """

    __slots__ = ("use", "maxdepth")

    cdef basestring _use
    cdef long _maxdepth

    @property
    def use(self):
        return self._use

    @property
    def maxdepth(self):
        return None if self._maxdepth == 0 else self._maxdepth

    def __init__(self, use, maxdepth=None, alias=None, replace=False):
        use = contracts.expect_basestr(self, "use", use)
        maxdepth = contracts.expect_length(self, "maxdepth", maxdepth, nullable=True)

        self._use = use
        self._maxdepth = 0 if maxdepth is None else maxdepth

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if __context is None:
            __context = {}  # Setup context, if it's top level call

        instance = instances.get(self.use)
        if self._maxdepth == 0:
            return instance(value, __context)

        cdef long depth
        try:
            key = self.use + ".recursion_depth"
            depth = __context.setdefault(key, 0) + 1
            if depth > self._maxdepth:
                raise exc.RecursionMaxDepthError(expected=self._maxdepth, actual=depth)
            __context[key] = depth
            return instance(value, __context)
        finally:
            __context[key] -= 1


cdef class Type(abstract.Validator):
    """
    Custom Type Validator

    :param type tp:
        valid value type.

    :param bool nullable:
        accept ``None`` as a valid value.

    :param bool coerce:
        try to convert value to ``tp``.

    :param tp min:
        lower limit, makes sense only if ``tp`` provides comparison methods.

    :param tp max:
        upper limit, makes sense only if ``tp`` provides comparison methods.

    :param int minlen:
        lower length limit, makes sense only if ``tp`` provides ``__len__()`` method.

    :param int maxlen:
        upper length limit, makes sense only if ``tp`` provides ``__len__()`` method.

    :param iterable options:
        explicit enumeration of valid values.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``not isinstance(value, self.tp)`` and ``not self.coerce``;
        * if ``self.tp(value)`` raises ``ValueError`` or ``TypeError``.

    :raises MinValueError:
        if ``value < self.min``.

    :raises MaxValueError:
        if ``value > self.max``.

    :raises MinLengthError:
        if ``len(value) < self.minlen``.

    :raises MaxLengthError:
        if ``len(value) > self.maxlen``.

    :raises OptionsError:
        if ``value not in self.options``.

    """

    __slots__ = (
        "tp",
        "nullable",
        "coerce",
        "min",
        "max",
        "minlen",
        "maxlen",
        "options",
    )

    cdef type _tp
    cdef bint _nullable
    cdef bint _coerce
    cdef object _min
    cdef object _max
    cdef long _minlen
    cdef long _maxlen
    cdef object _options

    @property
    def tp(self):
        return self._tp

    @property
    def nullable(self):
        return self._nullable

    @property
    def coerce(self):
        return self._coerce

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def minlen(self):
        return None if self._minlen == 0 else self._minlen

    @property
    def maxlen(self):
        return None if self._maxlen == limits.LONG_MAX else self._maxlen

    @property
    def options(self):
        return self._options

    def __init__(
        self,
        tp,
        nullable=False,
        coerce=False,
        min=None,
        max=None,
        minlen=None,
        maxlen=None,
        options=None,
        alias=None,
        replace=False,
    ):
        tp = contracts.expect(self, "tp", tp, types=type)
        nullable = contracts.expect_flag(self, "nullable", nullable)
        coerce = contracts.expect_flag(self, "coerce", coerce)
        min = contracts.expect(self, "min", min, types=tp, nullable=True)
        max = contracts.expect(self, "max", max, types=tp, nullable=True)
        minlen = contracts.expect_length(self, "minlen", minlen, nullable=True)
        maxlen = contracts.expect_length(self, "maxlen", maxlen, nullable=True)
        options = contracts.expect_container(
            self, "options", options, nullable=True, item_type=tp
        )

        if minlen is not None or maxlen is not None:
            if not hasattr(tp, "__len__"):
                raise TypeError("Type %r does not provide method '__len__()'" % tp)

        self._tp = tp
        self._nullable = nullable
        self._coerce = coerce
        self._min = min
        self._max = max
        self._minlen = 0 if minlen is None else minlen
        self._maxlen = limits.LONG_MAX if maxlen is None else maxlen
        self._options = options

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None and self.nullable:
            return value
        if not isinstance(value, self.tp):
            if not self.coerce:
                raise exc.InvalidTypeError(expected=self.tp, actual=type(value))
            else:
                try:
                    value = self.tp(value)
                except (TypeError, ValueError):
                    raise exc.InvalidTypeError(expected=self.tp, actual=type(value))
        if self.min is not None and value < self.min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if self.max is not None and value > self.max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        cdef long length
        if self.minlen is not None or self.maxlen is not None:
            length = len(value)
            if self.minlen is not None and length < self.minlen:
                raise exc.MinLengthError(expected=self.minlen, actual=length)
            if self.maxlen is not None and length > self.maxlen:
                raise exc.MaxLengthError(expected=self.maxlen, actual=length)
        if self.options is not None and value not in self.options:
            raise exc.OptionsError(expected=self.options, actual=value)
        return value


cdef class Const(abstract.Validator):
    """
    Constant Validator

    It only accepts single predefined value.


    :param value:
        expected valid value.


    :raises OptionsError:
        if ``value != self.value``.

    """

    __slots__ = ("value",)

    cdef object _value

    @property
    def value(self):
        return self._value

    def __init__(self, value, alias=None, replace=False):
        self._value = value
        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value != self.value:
            raise exc.OptionsError(expected=[self.value], actual=value)
        return value


cdef class Any(abstract.Validator):
    """
    Pass-Any Validator

    It literally accepts any value.

    """

    def __call__(self, value, __context=None):
        return value

