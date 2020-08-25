from libc cimport math
from libc cimport limits

from .. import exc
from .. import contracts
from ..compat.types import numbers
from . cimport abstract


cdef class Int(abstract.Validator):
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

    cdef bint _nullable
    cdef bint _coerce
    cdef long _min
    cdef long _max
    cdef frozenset _options

    @property
    def nullable(self):
        return self._nullable

    @property
    def coerce(self):
        return self._coerce

    @property
    def min(self):
        return None if self._min == limits.LONG_MIN else self._min

    @property
    def max(self):
        return None if self._max == limits.LONG_MAX else self._max

    @property
    def options(self):
        return self._options

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

        self._nullable = nullable
        self._coerce = coerce
        self._min = limits.LONG_MIN if min is None else min
        self._max = limits.LONG_MAX if max is None else max
        self._options = options

        self._register(alias, replace)

    def __call__(self, value, __context=None):
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
        cdef long _value = value
        if _value < self._min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if _value > self._max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        if self.options is not None and value not in self.options:
            raise exc.OptionsError(expected=self.options, actual=value)
        return value


cdef class Float(abstract.Validator):
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

    cdef bint _nullable
    cdef bint _coerce
    cdef bint _nan
    cdef bint _inf
    cdef double _min
    cdef double _max

    @property
    def nullable(self):
        return self._nullable

    @property
    def coerce(self):
        return self._coerce

    @property
    def nan(self):
        return self._nan

    @property
    def inf(self):
        return self._inf

    @property
    def min(self):
        return None if self._min == float("-inf") else self._min

    @property
    def max(self):
        return None if self._max == float("+inf") else self._max

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
            self, "min", min, nullable=True, types=numbers, convert_to=float
        )
        max = contracts.expect(
            self, "max", max, nullable=True, types=numbers, convert_to=float
        )

        self._nullable = nullable
        self._coerce = coerce
        self._nan = nan
        self._inf = inf
        self._min = float("-inf") if min is None else min
        self._max = float("+inf") if max is None else max

        self._register(alias, replace)

    def __call__(self, value, __context=None):
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
        cdef double _value = value
        if math.isnan(_value):
            if not self.nan:
                raise exc.FloatValueError(expected="number", actual=value)
            # It doesn't make sence to future checks if value is ``Nan``
            return value
        if math.isinf(_value) and not self.inf:
            raise exc.FloatValueError(expected="finite", actual=value)
        if _value < self._min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if _value > self._max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        return value
