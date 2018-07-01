from libc cimport math
from libc cimport limits

from .. import exc
from . cimport abstract


cdef class Int(abstract.Validator):

    __slots__ = ("nullable", "coerce", "min", "max", "options")

    cdef public bint nullable
    cdef public bint coerce
    cdef long _min
    cdef long _max
    cdef public options

    @property
    def min(self):
        return None if self._min == limits.LONG_MIN else self._min

    @min.setter
    def min(self, value):
        self._min = value if value is not None else limits.LONG_MIN

    @property
    def max(self):
        return None if self._max == limits.LONG_MAX else self._max

    @max.setter
    def max(self, value):
        self._max = value if value is not None else limits.LONG_MAX

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
        cdef long _value = value
        if _value < self._min:
            raise exc.MinValueError(expected=self.min, actual=value)
        if _value > self._max:
            raise exc.MaxValueError(expected=self.max, actual=value)
        if self.options is not None and value not in self.options:
            raise exc.OptionsError(expected=self.options, actual=value)
        return value


cdef class Float(abstract.Validator):

    __slots__ = ("nullable", "coerce", "nan", "inf", "min", "max")

    cdef public bint nullable
    cdef public bint coerce
    cdef public bint nan
    cdef public bint inf
    cdef public float _min
    cdef public float _max

    @property
    def min(self):
        return None if self._min == float("-inf") else self._min

    @min.setter
    def min(self, value):
        self._min = value if value is not None else float("-inf")

    @property
    def max(self):
        return None if self._max == float("inf") else self._max

    @max.setter
    def max(self, value):
        self._max = value if value is not None else float("inf")

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
        cdef float _value = value
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
