import collections as abc
import sys

try:
    import typing as t  # noqa
except ImportError:  # pragma: no cover
    pass

from .. import exc
from . import abstract


if sys.version_info[0] < 3:  # pragma: no cover
    str = unicode  # noqa


class List(abstract.Validator):

    __slots__ = ("item", "nullable", "minlen", "maxlen", "unique")

    def __init__(self, item, **kw):
        super(List, self).__init__(item=item, **kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, (list, tuple)):
            raise exc.InvalidTypeError(expected=(list, tuple), actual=type(value))
        length = len(value)
        if self.minlen is not None and length < self.minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if self.maxlen is not None and length > self.maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)

        result = []
        errors = []
        if self.unique:
            unique = set()

        for num, val in enumerate(value):
            try:
                val = self.item(val)
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
        return result


class Sequence(abstract.Validator):

    __slots__ = ("item", "nullable", "minlen", "maxlen", "unique")

    def __init__(self, item, **kw):
        super(Sequence, self).__init__(item=item, **kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, abc.Sequence) or isinstance(value, (str, bytes)):
            # Treat ``str`` and ``bytes`` like scalars
            raise exc.InvalidTypeError(expected=abc.Sequence, actual=type(value))
        length = len(value)
        if self.minlen is not None and length < self.minlen:
            raise exc.MinLengthError(expected=self.minlen, actual=length)
        if self.maxlen is not None and length > self.maxlen:
            raise exc.MaxLengthError(expected=self.maxlen, actual=length)

        result = []
        errors = []
        if self.unique:
            unique = set()

        for num, val in enumerate(value):
            try:
                val = self.item(val)
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
        return result


class Tuple(abstract.Validator):

    __slots__ = ("items", "nullable")

    def __init__(self, *items, **kw):
        super(Tuple, self).__init__(items=list(items), **kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, (list, tuple)):
            raise exc.InvalidTypeError(expected=(list, tuple), actual=type(value))
        if len(self.items) != len(value):
            raise exc.TupleLengthError(expected=len(self.items), actual=len(value))

        result = []
        errors = []

        for num, val in enumerate(value):
            try:
                val = self.items[num](val)
            except exc.ValidationError as e:
                errors.extend(ne.add_context(num) for ne in e)
                continue
            result.append(val)

        if errors:
            raise exc.SchemaError(errors)
        return tuple(result)
