from .. import exc
from . cimport abstract


cdef class Bool(abstract.Validator):

    TRUE = ("1", "true", "yes", "y", "on")
    FALSE = ("0", "false", "no", "n", "off")

    __slots__ = ("nullable", "coerce_str", "coerce_int")

    cdef public bint nullable
    cdef public bint coerce_str
    cdef public bint coerce_int

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
