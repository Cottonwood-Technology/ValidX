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
