import math
import decimal

from .. import contracts
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

    :param iterable options:
        explicit enumeration of valid values.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``not isinstance(value, int)`` and ``not self.coerce``.

    :raises CoerceError:
        if ``self.coerce`` and ``int(value)`` raises an exception.

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

    def __init__(
        self,
        nullable=False,
        coerce=False,
        min=None,
        max=None,
        options=None,
        alias=None,
        replace=False,
    ):
        nullable = contracts.expect_flag(self, "nullable", nullable)
        coerce = contracts.expect_flag(self, "coerce", coerce)
        min = contracts.expect(self, "min", min, nullable=True, types=int)
        max = contracts.expect(self, "max", max, nullable=True, types=int)
        options = contracts.expect_container(
            self, "options", options, nullable=True, item_type=int
        )

        setattr = object.__setattr__
        setattr(self, "nullable", nullable)
        setattr(self, "coerce", coerce)
        setattr(self, "min", min)
        setattr(self, "max", max)
        setattr(self, "options", options)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None and self.nullable:
            return value
        if not isinstance(value, int) or isinstance(value, bool):
            if isinstance(value, float) and value.is_integer():
                # Implicitly convert ``float`` to ``int``,
                # if the value represents integer number
                value = int(value)
            elif not self.coerce:
                raise exc.InvalidTypeError(expected=int, actual=type(value))
            else:
                try:
                    value = int(value)
                except Exception:
                    raise exc.CoerceError(expected=int, actual=value)
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
        * if ``not isinstance(value, float)`` and ``not self.coerce``.

    :raises CoerceError:
        if ``self.coerce`` and ``float(value)`` raises an exception.

    :raises NumberError:
        * if ``math.isnan(value)`` and ``not self.nan``;
        * if ``math.isinf(value)`` and ``not self.inf``.

    :raises MinValueError:
        if ``value < self.min``.

    :raises MaxValueError:
        if ``value > self.max``.


    :note: It always converts ``int`` to ``float``.

    """

    __slots__ = ("nullable", "coerce", "nan", "inf", "min", "max")

    def __init__(
        self,
        nullable=False,
        coerce=False,
        nan=False,
        inf=False,
        min=None,
        max=None,
        alias=None,
        replace=False,
    ):
        nullable = contracts.expect_flag(self, "nullable", nullable)
        coerce = contracts.expect_flag(self, "coerce", coerce)
        nan = contracts.expect_flag(self, "nan", nan)
        inf = contracts.expect_flag(self, "inf", inf)
        min = contracts.expect(
            self, "min", min, nullable=True, types=(int, float), convert_to=float
        )
        max = contracts.expect(
            self, "max", max, nullable=True, types=(int, float), convert_to=float
        )

        setattr = object.__setattr__
        setattr(self, "nullable", nullable)
        setattr(self, "coerce", coerce)
        setattr(self, "nan", nan)
        setattr(self, "inf", inf)
        setattr(self, "min", min)
        setattr(self, "max", max)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None and self.nullable:
            return value
        if not isinstance(value, float):
            if isinstance(value, int) and not isinstance(value, bool):
                try:
                    # Always implicitly convert ``int`` to ``float``
                    value = float(value)
                except OverflowError:
                    # Treat big numbers as infinity,
                    # in the same way as conversion from string does.
                    value = float("inf") if value > 0 else float("-inf")
            elif not self.coerce:
                raise exc.InvalidTypeError(expected=float, actual=type(value))
            else:
                try:
                    value = float(value)
                except Exception:
                    raise exc.CoerceError(expected=float, actual=value)
        if math.isnan(value):
            if not self.nan:
                raise exc.NumberError(expected="number", actual=value)
            # It doesn't make sence to future checks if value is ``Nan``
            return value
        if math.isinf(value) and not self.inf:
            raise exc.NumberError(expected="finite", actual=value)
        if self.min is not None and value < self.min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if self.max is not None and value > self.max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        return value


class Decimal(abstract.Validator):
    """
    Fixed Point Number Validator


    :param bool nullable:
        accept ``None`` as a valid value.

    :param bool coerce:
        try to convert non-decimal value to ``decimal.Decimal``.

    :param int precision:
        number of decimal places after point.

    :param bool nan:
        accept ``Not-a-Number`` as a valid value.

    :param bool inf:
        accept ``Infinity`` as a valid value.

    :param decimal.Decimal min:
        lower limit.

    :param decimal.Decimal max:
        upper limit.


    :raises InvalidTypeError:
        * if ``value is None`` and ``not self.nullable``;
        * if ``not isinstance(value, decimal.Decimal)`` and ``not self.coerce``.

    :raises CoerceError:
        if ``self.coerce`` and ``decimal.Decimal(value)`` raises an exception.

    :raises NumberError:
        * if ``value.is_nan()`` and ``not self.nan``;
        * if ``value.is_infinite()`` and ``not self.inf``.

    :raises MinValueError:
        if ``value < self.min``.

    :raises MaxValueError:
        if ``value > self.max``.


    :note: It always converts ``int`` and ``float`` to ``decimal.Decimal``.

    """

    __slots__ = ("nullable", "coerce", "precision", "nan", "inf", "min", "max")

    def __init__(
        self,
        nullable=False,
        coerce=False,
        precision=None,
        nan=False,
        inf=False,
        min=None,
        max=None,
        alias=None,
        replace=False,
    ):
        nullable = contracts.expect_flag(self, "nullable", nullable)
        coerce = contracts.expect_flag(self, "coerce", coerce)
        precision = contracts.expect(
            self,
            "precision",
            precision,
            nullable=True,
            types=int,
        )
        nan = contracts.expect_flag(self, "nan", nan)
        inf = contracts.expect_flag(self, "inf", inf)
        min = contracts.expect(
            self,
            "min",
            min,
            nullable=True,
            types=(int, float, str, decimal.Decimal),
            convert_to=decimal.Decimal,
        )
        max = contracts.expect(
            self,
            "max",
            max,
            nullable=True,
            types=(int, float, str, decimal.Decimal),
            convert_to=decimal.Decimal,
        )

        setattr = object.__setattr__
        setattr(self, "nullable", nullable)
        setattr(self, "coerce", coerce)
        setattr(self, "precision", precision)
        setattr(self, "nan", nan)
        setattr(self, "inf", inf)
        setattr(self, "min", min)
        setattr(self, "max", max)

        self._register(alias, replace)

    def __call__(self, value, __context=None):
        if value is None and self.nullable:
            return value
        if not isinstance(value, decimal.Decimal):
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                value = decimal.Decimal(value)
            elif not self.coerce:
                raise exc.InvalidTypeError(expected=decimal.Decimal, actual=type(value))
            else:
                try:
                    value = decimal.Decimal(value)
                except Exception:
                    raise exc.CoerceError(expected=decimal.Decimal, actual=value)
        if value.is_nan():
            if not self.nan:
                raise exc.NumberError(expected="number", actual=value)
            # It doesn't make sence to future checks if value is ``Nan``
            return value
        if value.is_infinite() and not self.inf:
            raise exc.NumberError(expected="finite", actual=value)
        if self.precision is not None and value.is_finite():
            with decimal.localcontext(decimal.BasicContext):
                value = round(value, self.precision)
        if self.min is not None and value < self.min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if self.max is not None and value > self.max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        return value
