try:
    import threading
except ImportError:  # pragma: no cover
    import dummy_threading as threading  # noqa

from .. import exc
from . import abstract, instances


class LazyRef(abstract.Validator):
    """
    Lazy Referenced Validator

    It is useful to build validators for recursive structures.

    It does not act as a pure function,
    it changes its state during validation.
    However,
    it is thread-safe.

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

    __slots__ = ("use", "maxdepth", "_state")

    def __init__(self, use, **kw):
        super(LazyRef, self).__init__(use=use, _state=threading.local(), **kw)

    def __call__(self, value):
        instance = instances.get(self.use)
        if self.maxdepth is None:
            return instance(value)
        state = self._state.__dict__
        try:
            depth = state.setdefault("depth", 0) + 1
            if depth > self.maxdepth:
                raise exc.RecursionMaxDepthError(expected=self.maxdepth, actual=depth)
            state["depth"] = depth
            return instance(value)
        finally:
            state["depth"] -= 1


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

    :param options:
        explicit enumeration of valid values.
    :type options: list or tuple


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

    def __init__(self, tp, **kw):
        super(Type, self).__init__(tp=tp, **kw)
        if self.minlen is not None or self.maxlen is not None:
            assert hasattr(tp, "__len__"), (
                "Type %r does not provide method '__len__()'" % tp
            )

    def __call__(self, value):
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

    def __init__(self, value, **kw):
        super(Const, self).__init__(value=value, **kw)

    def __call__(self, value):
        if value != self.value:
            raise exc.OptionsError(expected=[self.value], actual=value)
        return value


class Any(abstract.Validator):
    """
    Pass-Any Validator

    It literally accepts any value.
    The only optional check is for ``None`` values.


    :param bool nullable:
        accept ``None`` as a valid value.


    :raises InvalidTypeError:
        if ``value is None`` and ``not self.nullable``.

    """

    __slots__ = ("nullable",)

    def __call__(self, value):
        if value is None and not self.nullable:
            # TODO: isinstance(None, object) is True
            # Should there be some special handcrafted abstract base class?
            raise exc.InvalidTypeError(expected=object, actual=type(value))
        return value
