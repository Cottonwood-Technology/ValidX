import sys
from collections import Sequence

from .. import exc
from . import abstract


if sys.version_info[0] < 3:  # pragma: no cover
    str = unicode  # noqa


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

    def __init__(self, item, **kw):
        super(List, self).__init__(item=item, **kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, (list, tuple)):
            if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
                raise exc.InvalidTypeError(expected=Sequence, actual=type(value))
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
    """
    Tuple Validator


    :param Validator \*items:
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

    def __init__(self, *items, **kw):
        kw.setdefault("items", list(items))
        super(Tuple, self).__init__(**kw)

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, (list, tuple)):
            if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
                raise exc.InvalidTypeError(expected=Sequence, actual=type(value))
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
