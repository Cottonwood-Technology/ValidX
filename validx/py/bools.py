from .. import exc
from . import abstract


class Bool(abstract.Validator):
    """
    Boolean Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param bool coerce_str:
        * accept values ``["1", "true", "yes", "y", "on"]`` as ``True``;
        * accept values ``["0", "false", "no", "n", "off"]`` as ``False``.

    :param bool coerce_int:
        accept ``int`` as valid value.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``isinstance(value, str)`` and ``not self.coerce_str``;
        * if ``isinstance(value, int)`` and ``not self.coerce_int``;
        * if ``not isinstance(value, bool)``.

    :raises OptionsError:
        when string value is not valid name, see ``coerce_str``.

    """

    TRUE = ("1", "true", "yes", "y", "on")
    FALSE = ("0", "false", "no", "n", "off")

    __slots__ = ("nullable", "coerce_str", "coerce_int")

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, bool):
            if isinstance(value, str) and self.coerce_str:
                value = value.lower()
                if value in self.TRUE:
                    return True
                if value in self.FALSE:
                    return False
                raise exc.OptionsError(expected=self.TRUE + self.FALSE, actual=value)
            elif isinstance(value, int) and self.coerce_int:
                return bool(value)
            raise exc.InvalidTypeError(expected=bool, actual=type(value))
        return value
