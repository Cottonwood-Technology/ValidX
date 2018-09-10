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

    ..  warning::

        It is not thread safe,
        use :class:`LazyRefTS` in multithreading applications.

    ..  testsetup:: lazyref

        from validateit import Dict, Int, LazyRef, instances

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
        validateit.exc.errors.SchemaError: <SchemaError(errors=[
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

    __slots__ = ("use", "maxdepth", "_depth")

    def __init__(self, use, **kw):
        super(LazyRef, self).__init__(use=use, _depth=0, **kw)

    def __call__(self, value):
        try:
            self._depth += 1
            if self.maxdepth is not None and self._depth > self.maxdepth:
                raise exc.RecursionMaxDepthError(
                    expected=self.maxdepth, actual=self._depth
                )
            return instances.get(self.use)(value)
        finally:
            self._depth -= 1


class LazyRefTS(abstract.Validator):
    """
    Lazy Referenced Validator, Thread Safe Version

    It is useful to build validators for recursive structures.

    ..  testsetup:: lazyrefts

        from validateit import Dict, Int, LazyRefTS, instances

    ..  testcleanup:: lazyrefts

        instances.clear()

    ..  doctest:: lazyrefts
        :options: +ELLIPSIS, -IGNORE_EXCEPTION_DETAIL

        >>> schema = Dict(
        ...     {
        ...         "foo": Int(),
        ...         "bar": LazyRefTS("schema", maxdepth=1),
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
        validateit.exc.errors.SchemaError: <SchemaError(errors=[
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

    __slots__ = ("use", "maxdepth", "_depth")

    def __init__(self, use, **kw):
        super(LazyRefTS, self).__init__(use=use, _depth=threading.local(), **kw)

    def __call__(self, value):
        try:
            depth = self._depth.__dict__.setdefault("value", 0)
            depth += 1
            self._depth.value = depth
            if self.maxdepth is not None and depth > self.maxdepth:
                raise exc.RecursionMaxDepthError(expected=self.maxdepth, actual=depth)
            return instances.get(self.use)(value)
        finally:
            self._depth.value -= 1


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
