import math

from .. import exc
from . import abstract


class Int(abstract.Validator):
    """
    Integer Number Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param bool coerce:
        try to convert non-integer value to ``int``.

    :param int min:
        lower limit.

    :param int max:
        upper limit.

    :param options:
        explicit enumeration of valid values.
    :type options: list or tuple


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``not isinstance(value, int)`` and ``not self.coerce``;
        * if ``int(value)`` raises ``ValueError`` or ``TypeError``.

    :raises MinValueError:
        if ``value < self.min``.

    :raises MaxValueError:
        if ``value > self.max``.

    :raises OptionsError:
        if ``value not in self.options``.


    :note:
        It implicitly converts ``float`` to ``int``,
        if ``value.is_integer() is True``.

    """

    __slots__ = ("nullable", "coerce", "min", "max", "options")

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, int):
            if isinstance(value, float) and value.is_integer():
                # Implicitly convert ``float`` to ``int``,
                # if the value represents integer number
                value = int(value)
            elif not self.coerce:
                raise exc.InvalidTypeError(expected=int, actual=type(value))
            else:
                try:
                    value = int(value)
                except (TypeError, ValueError):
                    raise exc.InvalidTypeError(expected=int, actual=type(value))
        if self.min is not None and value < self.min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if self.max is not None and value > self.max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        if self.options is not None and value not in self.options:
            raise exc.OptionsError(expected=self.options, actual=value)
        return value


class Float(abstract.Validator):
    """
    Floating Point Number Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param bool coerce:
        try to convert non-float value to ``float``.

    :param bool nan:
        accept ``Not-a-Number`` as a valid value.

    :param bool inf:
        accept ``Infinity`` as a valid value.

    :param float min:
        lower limit.

    :param float max:
        upper limit.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``not isinstance(value, float)`` and ``not self.coerce``;
        * if ``float(value)`` raises ``ValueError`` or ``TypeError``.

    :raises FloatValueError:
        * if ``math.isnan(value)`` and ``not self.nan``;
        * if ``math.isinf(value)`` and ``not self.inf``.

    :raises MinValueError:
        if ``value < self.min``.

    :raises MaxValueError:
        if ``value > self.max``.


    :note: It always converts ``int`` to ``float``.

    """

    __slots__ = ("nullable", "coerce", "nan", "inf", "min", "max")

    def __call__(self, value):
        if value is None and self.nullable:
            return value
        if not isinstance(value, float):
            if isinstance(value, int):
                # Always implicitly convert ``int`` to ``float``
                value = float(value)
            elif not self.coerce:
                raise exc.InvalidTypeError(expected=float, actual=type(value))
            else:
                try:
                    value = float(value)
                except (TypeError, ValueError):
                    raise exc.InvalidTypeError(expected=float, actual=type(value))
        if math.isnan(value):
            if not self.nan:
                raise exc.FloatValueError(expected="number", actual=value)
            # It doesn't make sence to future checks if value is ``Nan``
            return value
        if math.isinf(value) and not self.inf:
            raise exc.FloatValueError(expected="finite", actual=value)
        if self.min is not None and value < self.min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if self.max is not None and value > self.max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        return value
