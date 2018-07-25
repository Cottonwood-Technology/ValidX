from .. import exc
from . cimport abstract


cdef class Any(abstract.Validator):

    __slots__ = ("nullable",)

    cdef public bint nullable

    def __call__(self, value):
        if value is None and not self.nullable:
            # TODO: isinstance(None, object) is True
            # Should there be some special handcrafted abstract base class?
            raise exc.InvalidTypeError(expected=object, actual=type(value))
        return value
