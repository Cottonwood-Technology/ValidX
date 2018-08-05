from .. import exc
from . import abstract


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
