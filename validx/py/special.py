from .. import exc
from .. import contracts
from . import abstract, instances


class LazyRef(abstract.Validator):
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

    def __init__(self, use, maxdepth=None, alias=None, replace=False):
        use = contracts.expect_str(self, "use", use)
        maxdepth = contracts.expect_length(self, "maxdepth", maxdepth, nullable=True)

        setattr = object.__setattr__
        setattr(self, "use", use)
        setattr(self, "maxdepth", maxdepth)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if __context is None:
            __context = {}  # Setup context, if it's top level call

        instance = instances.get(self.use)
        if self.maxdepth is None:
            return instance(value, __context)

        try:
            key = self.use + ".recursion_depth"
            depth = __context.setdefault(key, 0) + 1
            if depth > self.maxdepth:
                raise exc.RecursionMaxDepthError(expected=self.maxdepth, actual=depth)
            __context[key] = depth
            return instance(value, __context)
        finally:
            __context[key] -= 1


class Type(abstract.Validator):
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
        * if ``not isinstance(value, self.tp)`` and ``not self.coerce``.

    :raises CoerceError:
        if ``self.coerce`` and ``tp(value)`` raises an exception.

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

        setattr = object.__setattr__
        setattr(self, "tp", tp)
        setattr(self, "nullable", nullable)
        setattr(self, "coerce", coerce)
        setattr(self, "min", min)
        setattr(self, "max", max)
        setattr(self, "minlen", minlen)
        setattr(self, "maxlen", maxlen)
        setattr(self, "options", options)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None:
            if self.nullable:
                return value
            raise exc.InvalidTypeError(expected=self.tp, actual=type(value))
        if not isinstance(value, self.tp):
            if not self.coerce:
                raise exc.InvalidTypeError(expected=self.tp, actual=type(value))
            else:
                try:
                    value = self.tp(value)
                except Exception:
                    raise exc.CoerceError(expected=self.tp, actual=value)
        if self.min is not None and value < self.min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if self.max is not None and value > self.max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        if self.minlen is not None or self.maxlen is not None:
            length = len(value)
            if self.minlen is not None and length < self.minlen:
                raise exc.MinLengthError(expected=self.minlen, actual=length)
            if self.maxlen is not None and length > self.maxlen:
                raise exc.MaxLengthError(expected=self.maxlen, actual=length)
        if self.options is not None and value not in self.options:
            raise exc.OptionsError(expected=self.options, actual=value)
        return value


class Const(abstract.Validator):
    """
    Constant Validator

    It only accepts single predefined value.


    :param value:
        expected valid value.


    :raises OptionsError:
        if ``value != self.value``.

    """

    __slots__ = ("value",)

    def __init__(self, value, alias=None, replace=False):
        setattr = object.__setattr__
        setattr(self, "value", value)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value != self.value:
            raise exc.OptionsError(expected=[self.value], actual=value)
        return value

    def params(self):
        yield "value", self.value


class Any(abstract.Validator):
    """
    Pass-Any Validator

    It literally accepts any value.

    """

    def __call__(self, value, __context=None):
        return value
